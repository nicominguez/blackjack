from src.rules import HouseRules
from src.player import *
from src.game import Game

def main():
    rules = HouseRules()
    player = ChartPlayer2()
    game = Game(rules, player)
    result = game.play_round(bet_amount = 5)
    print(f"Outcome: {result.get("outcome")} \n\nPlayer's hand: {result.get("player")} \n\nDealer's hand: {result.get("dealer")} \n\nBankroll: {result.get("bankroll")}")

if __name__ == "__main__":
    main()