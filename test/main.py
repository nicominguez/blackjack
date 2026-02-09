from src.simulation import run_sim
from src.player import ChartPlayer2, RCHighLowPlayer, QLearningPlayer
from src.rules import HouseRules

def main():
    q_player = QLearningPlayer(training_mode=False)
    q_player.load_model("../models/q_learning_player.pkl")

    PARAMETERS = {
        "players": [ChartPlayer2(), RCHighLowPlayer(), q_player],
        "rules": HouseRules(),
        "num_hands": 100000,
        "BASE_BET": 5,
        "plot_bh": True,
        "plot_wr": True
    }

    results = run_sim(**PARAMETERS)
    for result in results:
        print(f"Player: {result['player']}")
        print(f"Hands played: {result['total_games']}")
        print(f"Wins: {result['wins']} ~ {(result['wins']/result['total_games']):.2%}")
        print(f"Losses: {result['losses']} ~ {(result['losses']/result['total_games']):.2%}")
        print(f"Pushes: {result['pushes']} ~ {(result['pushes']/result['total_games']):.2%}")
        print(f"Bankroll: {result['final_bankroll']}\n")


if __name__ == "__main__":
    main()
