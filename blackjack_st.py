import streamlit as st
import pandas as pd
from pathlib import Path
import inspect
import re

from blackjack.src.simulation import run_sim
import blackjack.src.players as player_mod
from blackjack.src.rules import HouseRules

st.set_page_config(
    page_title="Blackjack Simulation",
    page_icon="🃏",
    layout="wide",
)

PLAYER_METADATA = {
    "RandomStrategyPlayer": ("Random Strategy", 1),
    "BasicStrategyPlayer": ("Basic Strategy", 2),
    "ChartPlayer1": ("Chart Player 1", 3),
    "ChartPlayer2": ("Chart Player 2", 4),
    "RCHighLowPlayer": ("Running Count High Low", 5),
    "QLearningPlayer": ("Q-Learning AI", 6),
}


def _build_strategy_options():
    player_classes = [
        cls
        for _, cls in inspect.getmembers(player_mod, inspect.isclass)
        if issubclass(cls, player_mod.Player) and cls is not player_mod.Player
    ]

    options = {}
    for cls in player_classes:
        class_name = cls.__name__
        if class_name in PLAYER_METADATA:
            display_name, _ = PLAYER_METADATA[class_name]
        else:  # Fallback
            display_name = (
                re.sub(r"(?<!^)(?=[A-Z])", " ", class_name)
                .replace(" Player", "")
                .strip()
            )
        options[display_name] = cls

    return options


STRATEGY_OPTIONS = _build_strategy_options()

STRATEGY_OPTIONS_SORTED = dict(
    sorted(
        STRATEGY_OPTIONS.items(),
        key=lambda item: PLAYER_METADATA.get(item[1].__name__, (0, 0))[1],
        reverse=False,
    )
)

RULE_OPTIONS = {
    "Standard House Rules": HouseRules(),
}

PLAYER_COLORS = ["blue", "red", "green", "orange"]

if "num_players" not in st.session_state:
    st.session_state.num_players = 1


def render_player_settings(player_num):
    color = PLAYER_COLORS[player_num - 1]
    st.subheader(f":{color}[Player {player_num}]", divider=color)

    col1, col2 = st.columns(2)

    with col1:
        strategy = st.selectbox(
            "Strategy",
            options=list(STRATEGY_OPTIONS_SORTED.keys()),
            key=f"strategy_{player_num}",
            help="Choose the strategy the player will use",
        )

    with col2:
        rules = st.selectbox(
            "House Rules",
            options=list(RULE_OPTIONS.keys()),
            key=f"rules_{player_num}",
            help="Select the house rules",
        )

    return strategy, rules


def render_detailed_metrics(result, bankroll_history, color):
    with st.expander(f":{color}[Detailed Metrics]"):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"**Final Bankroll**  \n${bankroll_history[-1]:.0f}")

        with col2:
            st.markdown(f"**Starting Bankroll**  \n${bankroll_history[0]:.0f}")

        with col3:
            st.markdown(f"**Peak Bankroll**  \n${max(bankroll_history):.0f}")

        with col4:
            st.markdown(f"**Minimum Bankroll**  \n${min(bankroll_history):.0f}")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"**Total Hands**  \n{result.get('total_games', 0)}")

        with col2:
            win_rate = (result.get("wins", 0) / result.get("total_games", 1)) * 100
            st.markdown(f"**Win Rate**  \n{win_rate:.1f}%")

        with col3:
            st.markdown(f"**Wins**  \n{result.get('wins', 0)}")

        with col4:
            st.markdown(f"**Losses**  \n{result.get('losses', 0)}")


st.title("Blackjack")
st.markdown(
    "Simulate different blackjack player strategies and analyze their performance."
)

st.header("Simulation Settings")

player_configs = []
for i in range(1, st.session_state.num_players + 1):
    strategy, rules = render_player_settings(i)
    player_configs.append((strategy, rules))

if st.session_state.num_players < 4:
    if st.button("Add Player", type="tertiary", use_container_width=True):
        st.session_state.num_players += 1
        st.rerun()

for i, (strategy, _) in enumerate(player_configs):
    if strategy == "Q-Learning AI":
        model_path = Path("blackjack/_models/q_learning_player.pkl")

        col1, col2 = st.columns([3, 1])
        with col1:
            if model_path.exists():
                st.caption(
                    f"ℹ️ Player {i + 1}: Model loaded ({model_path.stat().st_size // 1024} KB)"
                )
            else:
                st.caption(f"⚠️ Player {i + 1}: No trained model found at {model_path}")

st.divider()

num_hands = st.slider(
    "Number of Hands to Simulate",
    min_value=10,
    max_value=10000,
    value=1000,
    step=10,
    help="How many hands should each player play?",
)

if st.button(
    "Run Simulation", key="run_sim_button", type="primary", use_container_width=True
):
    players = []
    model_path = Path("blackjack/_models/q_learning_player.pkl")

    for strategy, _ in player_configs:
        cls = STRATEGY_OPTIONS_SORTED[strategy]
        if cls.__name__ == "QLearningPlayer":
            p = cls(bankroll=1000, training_mode=False, epsilon=0.0)
            p.load_model(str(model_path))

        else:
            try:
                p = cls(bankroll=1000)
            except TypeError:
                p = cls()
        players.append(p)

    rules = RULE_OPTIONS[player_configs[0][1]]

    with st.spinner("Running simulation..."):
        results = run_sim(players=players, rules=rules, num_hands=num_hands)

    st.header("Simulation Results")

    if results and all(r.get("bankroll_history") for r in results):
        max_len = max(len(r["bankroll_history"]) for r in results)
        padded_data = {}
        for i, r in enumerate(results):
            history = r["bankroll_history"]
            if len(history) < max_len:
                history = history + [history[-1]] * (max_len - len(history))
            padded_data[f"Player {i + 1}"] = history

        df = pd.DataFrame(padded_data)
        st.line_chart(
            df,
            color=["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e"][: len(results)],
            use_container_width=True,
        )

        cols = st.columns(len(results))

        profits = [
            r["bankroll_history"][-1] - r["bankroll_history"][0] for r in results
        ]
        best_player_idx = profits.index(max(profits))

        for i, (result, col, color) in enumerate(zip(results, cols, PLAYER_COLORS)):
            bankroll_history = result["bankroll_history"]
            final_profit = bankroll_history[-1] - bankroll_history[0]
            profit_pct = (
                (final_profit / bankroll_history[0]) * 100
                if bankroll_history[0] > 0
                else 0
            )
            win_rate = (result.get("wins", 0) / result.get("total_games", 1)) * 100
            winner_mark = " 🏆" if i == best_player_idx else ""

            with col:
                st.markdown(f"### :{color}[Player {i + 1}]")
                st.metric("Win Rate", f"{win_rate:.1f}%")

                if final_profit >= 0:
                    st.success(
                        f"**Profit:** ${final_profit:+.0f} ({profit_pct:+.1f}%) {winner_mark}"
                    )
                else:
                    st.error(
                        f"**Loss:** ${final_profit:+.0f} ({profit_pct:+.1f}%) {winner_mark}"
                    )

                render_detailed_metrics(result, bankroll_history, color)
    else:
        st.error("Simulation failed to produce results.")
