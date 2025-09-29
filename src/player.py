from abc import ABC, abstractmethod
from src.card import Card
from src.hand import Hand
from src.rules import HouseRules
from src.player_utils import *
from typing import Literal
import random


class Player(ABC):
    def __init__(self, bankroll: int = 1000):
        self.bankroll = bankroll

    @abstractmethod
    def decide_move(self, hand: Hand, dealer_up: str, rules: HouseRules) -> Literal["hit", "stand", "double", "surrender"]:
        """Return one of: 'hit', 'stand', 'double', 'split', 'surrender'"""
        pass


class RandomStrategyPlayer(Player):
    def __repr__(self):
        return "Random"
    
    def decide_move(self, hand: Hand, dealer_up: str, rules: HouseRules) -> str:
        options = ["hit", "stand", "double", "split", "surrender"]
        return random.choice(options)


class BasicStrategyPlayer(Player):
    def __repr__(self):
        return "Basic Hit/Stand"

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
    def __repr__(self):
        return "Chart Player 1"

    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules):
        return map_result_char(BASIC_MATRIX[hand.best_total - 4][get_dealer_index(card_val = dealer_up.rank)])


class ChartPlayer2(Player):
    def __repr__(self):
        return "Chart Player 2"
    
    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules):
        if hand.is_soft:
            return map_result_char(SOFT_MATRIX[hand.best_total - 13][get_dealer_index(card_val = dealer_up.rank)])
        else:
            return map_result_char(HARD_MATRIX[hand.best_total - 4][get_dealer_index(card_val = dealer_up.rank)])