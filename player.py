from abc import ABC, abstractmethod
from hand import Hand
from rules import HouseRules

class Player(ABC):
    @abstractmethod
    def decide_move(self, hand: Hand, dealer_up, rules: HouseRules) -> str:
        """Return one of: 'hit', 'stand', 'double', 'split', 'surrender'"""
        pass

import random
class RandomStrategyPlayer(Player):
    def decide_move(self, hand: Hand, dealer_up, rules:HouseRules) -> str:
        options = ['hit', 'stand', 'double', 'split', 'surrender']
        return random.choice(options)
