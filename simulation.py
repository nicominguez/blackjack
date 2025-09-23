from player import RandomStrategyPlayer
from rules import HouseRules
from game import Game

def run_simulation(num_hands = 1000) -> None:
    wins, losses, pushes = 0, 0, 0

    p = RandomStrategyPlayer()
    r = HouseRules()
    game = Game(player=p, rules=r)

    for _ in range(num_hands):
        outcome = game.play_round()

        if outcome.get("outcome") == "win" or outcome.get("blackjack") == "win":
            wins += 1
        elif outcome.get("outcome") == "loss":
            losses += 1
        else:
            pushes += 1

    return [wins, losses, pushes, wins+losses+pushes, p.bankroll]

def main():
    results = run_simulation()

    print(f"Hands played: {results[3]}")
    print(f"Wins: {results[0]} ~ {(results[0]/results[3]):.2%}")
    print(f"Losses: {results[1]} ~ {(results[1]/results[3]):.2%}")
    print(f"Pushes: {results[2]} ~ {(results[2]/results[3]):.2%}")
    print(f"Bankroll: {results[4]}")

if __name__ == "__main__":
    main()