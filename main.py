from rules import HouseRules
from player import RandomStrategyPlayer
from game import Game

def main():
    rules = HouseRules()
    player = RandomStrategyPlayer()
    game = Game(rules, player)
    result = game.play_round(bet_amount = 5)
    print(f"Outcome: {result.get("outcome")} \n\nPlayer's hand: {result.get("player")} \n\nDealer's hand: {result.get("dealer")} \n\nBankroll: {result.get("bankroll")}")

if __name__ == "__main__":
    main()