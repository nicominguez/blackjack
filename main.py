from src.player import *
from src.rules import HouseRules
from src.game import Game
from plot import *

def run_sim(
        players: list[Player],
        rules: HouseRules = HouseRules(),
        num_hands: int = 1000,
        BASE_BET: int = 5,
        plot_bh: bool = False,
        plot_wr: bool = False
) -> list[dict[str, int | list]]:
    results = []
    bankroll_histories = []
    cumulative_winrates = []
    labels = []

    for player in players:
        game = Game(player=player, rules=rules, bet=BASE_BET)
        wins, losses, pushes = 0, 0, 0
        bankroll_history, cum_winrate = [], []

        for _ in range(num_hands):
            game.bet = game.player.decide_bet_amount(curr_bet_unit=BASE_BET, shoe_length=len(game.shoe))
            outcome = game.play_round()
            game.bet = BASE_BET #resets

            if outcome.get("outcome") == "broke":
                print(
                    f"Player {repr(player)} doesn't have money for the current bet.\n"
                    f"Player bankroll: {game.player.bankroll}\nCurrent bet: {BASE_BET}\n\n\n"
                )   
                break

            if outcome.get("outcome") in ["win", "blackjack"]:
                wins += 1
            elif outcome.get("outcome") in ["loss", "surr_loss"]:
                losses += 1
            else:
                pushes += 1

            bankroll_history.append(player.bankroll)
            cum_winrate.append(wins / (wins + losses + pushes))

        bankroll_histories.append(bankroll_history)
        cumulative_winrates.append(cum_winrate)
        labels.append(repr(player))

        results.append({
            "player": repr(player),
            "wins": wins,
            "losses": losses,
            "pushes": pushes,
            "total_games": wins + losses + pushes,
            "final_bankroll": player.bankroll,
            "bankroll_history": bankroll_history,
            "cum_winrate": cum_winrate,
        })

    # Plots
    if plot_bh:
        plot_bankroll_histories(bankroll_histories, labels)
    if plot_wr:
        plot_cumulative_winrates(cumulative_winrates, labels)

    return results


def main():
    PARAMETERS = {
        "players": [ChartPlayer2(), RCHighLowPlayer()],
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
