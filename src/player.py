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

    @abstractmethod
    def decide_bet_amount(self, curr_bet_unit: int, player_hand: Hand, dealer_hand: Hand, rules: HouseRules, shoe_length: int) -> int:
        """Returns bet amount for the following hand."""
        pass


class RandomStrategyPlayer(Player):
    def __repr__(self):
        return "Random"
    
    def decide_move(self, hand: Hand, dealer_up: str, rules: HouseRules) -> Literal["hit", "stand", "double", "surrender"]:
        options = ["hit", "stand", "double", "surrender"]
        return random.choice(options)
    
    def decide_bet_amount(self):
        pass


class BasicStrategyPlayer(Player):
    def __repr__(self):
        return "Basic Hit/Stand"

    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules) -> Literal["hit", "stand", "double", "surrender"]:
        if hand.best_total >= 17:
            return "stand"
        elif hand.best_total < 12:
            return "hit"
        else:
            if dealer_up.hard_value < 7:
                return "stand"
            else:
                return "hit"
            
    def decide_bet_amount(self, curr_bet_unit: int) -> int:
        return curr_bet_unit


class ChartPlayer1(Player):
    def __repr__(self):
        return "Chart Player 1"

    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules) -> Literal["hit", "stand", "double", "surrender"]:
        return map_result_char(BASIC_MATRIX[hand.best_total - 4][get_dealer_index(card_val = dealer_up.rank)])

    def decide_bet_amount(self, curr_bet_unit: int) -> int:
        return curr_bet_unit


class ChartPlayer2(Player):
    def __repr__(self):
        return "Chart Player 2"
    
    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules) -> Literal["hit", "stand", "double", "surrender"]:
        if hand.is_soft:
            return map_result_char(SOFT_MATRIX[hand.best_total - 13][get_dealer_index(card_val = dealer_up.rank)])
        else:
            return map_result_char(HARD_MATRIX[hand.best_total - 4][get_dealer_index(card_val = dealer_up.rank)])
        
    def decide_bet_amount(self, curr_bet_unit: int, shoe_length: int) -> int:
        return curr_bet_unit
    

class RCHighLowPlayer(Player):
    def __init__(self, bankroll = 1000):
        super().__init__(bankroll)
        self.running_count: int = 0

    def __repr__(self):
        return "Running Count High Low Player"
    
    def _update_running_count(self, card: Card | str) -> None:
        if type(card) == type(""):
            rank = card
        else:
            rank = card.rank
        if rank in ["2","3","4","5","6"]:
            self.running_count += 1
        elif rank in ["10","J","Q","K","A"]:
            self.running_count -= 1

    def _reset_running_count(self):
        self.running_count = 0
    
    def decide_move(self, hand, dealer_up, rules) -> Literal["hit", "stand", "double", "surrender"]: # same as CP2
        self._update_running_count(hand.cards[0].rank)
        self._update_running_count(hand.cards[1].rank)
        self._update_running_count(dealer_up)
        if hand.is_soft:
            return map_result_char(SOFT_MATRIX[hand.best_total - 13][get_dealer_index(card_val = dealer_up.rank)])
        else:
            return map_result_char(HARD_MATRIX[hand.best_total - 4][get_dealer_index(card_val = dealer_up.rank)])

    def decide_bet_amount(self, curr_bet_unit: int, shoe_length: int) -> int:
        true_count = self.running_count / max((shoe_length // 52),1) # avoid division by 0
        return max(int((true_count - 1) * curr_bet_unit), 5)