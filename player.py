from abc import ABC, abstractmethod
from card import Card
from hand import Hand
from rules import HouseRules
import random


class Player(ABC):
    def __init__(self, bankroll: int = 1000):
        self.bankroll = bankroll

    @abstractmethod
    def decide_move(self, hand: Hand, dealer_up: str, rules: HouseRules) -> str:
        """Return one of: 'hit', 'stand', 'double', 'split', 'surrender'"""
        pass


class RandomStrategyPlayer(Player):
    def decide_move(self, hand: Hand, dealer_up: str, rules: HouseRules) -> str:
        options = ["hit", "stand", "double", "split", "surrender"]
        return random.choice(options)


class BasicStrategyPlayer(Player):
    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules):
        if hand.best_total >= 17:
            return "stand"
        elif hand.best_total < 12:
            return "hit"
        else:
            if dealer_up.hard_value < 7:
                return "stand"
            else:
                return "hit"


class ChartPlayer1(Player):
    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules):
        hard_soft_matrix = [
            # 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10,'A'
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 4
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 5
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 6
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 7
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 8
            ["d", "d", "d", "d", "d", "h", "h", "h", "h", "h"],  # 9
            ["d", "d", "d", "d", "d", "h", "h", "h", "h", "h"],  # 10
            ["d", "d", "d", "d", "d", "h", "h", "h", "h", "h"],  # 11
            ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 12
            ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 13
            ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 14
            ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 15
            ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 16
            ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 17
            ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 18
            ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 19
            ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 20
            ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 21
        ]
        return hard_soft_matrix[hand.best_total - 4][
            dealer_up.rank - 2 if type(dealer_up.rank) == "int" else 9
        ]
