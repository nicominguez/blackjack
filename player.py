from abc import ABC, abstractmethod
from hand import Hand
from rules import HouseRules
import random

class Player(ABC):
    def __init__(self, bankroll: int = 1000):
        self.bankroll = bankroll

    @abstractmethod
    def decide_move(self, hand: Hand, dealer_up, rules: HouseRules) -> str:
        """Return one of: 'hit', 'stand', 'double', 'split', 'surrender'"""
        pass

class RandomStrategyPlayer(Player):
    def decide_move(self, hand: Hand, dealer_up, rules:HouseRules) -> str:
        options = ['hit', 'stand', 'double', 'split', 'surrender']
        ##return random.choice(options)
        return 'double'