from rules import HouseRules
from player import RandomStrategyPlayer
from game import Game

def main():
    rules = HouseRules()
    player = RandomStrategyPlayer()
    game = Game(rules, player)
    game.play_round()

if __name__ == "__main__":
    main()