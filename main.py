from src.player import *
from src.rules import HouseRules
from src.game import Game
from plot import *

def run_sim(
        player: Player = BasicStrategyPlayer(),
        rules: HouseRules = HouseRules(),
        num_hands: int = 1000,
        bet_amount: int = 5,
        plot_bh: bool = False,
        plot_wr: bool = False
) -> dict[str, int | list]:
    game = Game(player = player, rules = rules)

    wins, losses, pushes = 0, 0, 0
    bankroll_history, cum_winrate = [], []  # plots

    for _ in range(num_hands):
        outcome = game.play_round(bet_amount=bet_amount)

        if outcome.get("outcome") == "broke":
            print(
                f"Player doesn't have money for the current bet.\nPlayer bankroll: {game.player.bankroll}\nCurrent bet: {bet_amount}\n\n\n"
            )
            break

        if outcome.get("outcome") == "win" or outcome.get("outcome") == "blackjack":
            wins += 1
        elif outcome.get("outcome") == "loss":
            losses += 1
        else:
            pushes += 1

        bankroll_history.append(player.bankroll)
        cum_winrate.append(wins / (wins + losses + pushes))

    # Plots
    if plot_bh:
        plot_bankroll_histories([bankroll_history], [repr(player)])
    if plot_wr:
        plot_cumulative_winrates([cum_winrate], [repr(player)])

    return {
        "wins": wins,
        "losses": losses,
        "pushes": pushes,
        "total_games": wins + losses + pushes,
        "final_bankroll": player.bankroll,
        "bankroll_history": bankroll_history,
        "cum_winrate": cum_winrate,
    }



def main():
    PARAMETERS = {
        "player": ChartPlayer2(),
        "rules": HouseRules(),
        "num_hands": 3000,
        "bet_amount": 5,
        "plot_bh": False,
        "plot_wr": True
    }
    
    results = run_sim(**PARAMETERS)
    print(f"Hands played: {results.get("total_games")}")
    print(f"Wins: {results.get("wins")} ~ {(results.get("wins")/results.get("total_games")):.2%}")
    print(f"Losses: {results.get("losses")} ~ {(results.get("losses")/results.get("total_games")):.2%}")
    print(f"Pushes: {results.get("pushes")} ~ {(results.get("pushes")/results.get("total_games")):.2%}")
    print(f"Bankroll: {results.get("final_bankroll")}")


if __name__ == "__main__":
    main()
