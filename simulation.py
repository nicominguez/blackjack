from player import *
from rules import HouseRules
from game import Game

player = BasicStrategyPlayer() # default
rules = HouseRules() # default

def run_simulation(p: Player = player, r: HouseRules = rules, num_hands: int = 1000, bet_amount: int = 5) -> None:
    game = Game(player=p, rules=r)

    wins, losses, pushes = 0, 0, 0
    bankroll_history = [] # plots

    for _ in range(num_hands):
        outcome = game.play_round(bet_amount = bet_amount)

        if outcome.get("outcome") == "broke":
            print(f"Player doesn't have money for the current bet.\nPlayer bankroll: {game.player.bankroll}\nCurrent bet: {bet_amount}\n\n\n")
            break

        if outcome.get("outcome") == "win" or outcome.get("outcome") == "blackjack":
            wins += 1
        elif outcome.get("outcome") == "loss":
            losses += 1
        else:
            pushes += 1
        
        bankroll_history.append(p.bankroll)

    return [wins, losses, pushes, wins+losses+pushes, p.bankroll, bankroll_history]

def main():
    results = run_simulation(p = ChartPlayer2())

    print(f"Hands played: {results[3]}")
    print(f"Wins: {results[0]} ~ {(results[0]/results[3]):.2%}")
    print(f"Losses: {results[1]} ~ {(results[1]/results[3]):.2%}")
    print(f"Pushes: {results[2]} ~ {(results[2]/results[3]):.2%}")
    print(f"Bankroll: {results[4]}")
if __name__ == "__main__":
    main()