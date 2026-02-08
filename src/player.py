from abc import ABC, abstractmethod
from .card import Card
from .hand import Hand
from .rules import HouseRules
from .player_utils import *
from typing import Literal, Union
import random
import pickle
import os


class Player(ABC):
    def __init__(self, bankroll: int = 1000):
        self.bankroll = bankroll

    @abstractmethod
    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules) -> Literal["hit", "stand", "double", "surrender"]:
        pass

    @abstractmethod
    def decide_bet_amount(self, curr_bet_unit: int, shoe_length: int) -> int:
        pass


class RandomStrategyPlayer(Player):
    def __repr__(self):
        return "Random"
    
    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules) -> Literal["hit", "stand", "double", "surrender"]:
        options = ["hit", "stand", "double", "surrender"]
        return random.choice(options)
    
    def decide_bet_amount(self, curr_bet_unit: int, shoe_length: int) -> int:
        return curr_bet_unit


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
            
    def decide_bet_amount(self, curr_bet_unit: int, shoe_length: int) -> int:
        return curr_bet_unit


class ChartPlayer1(Player):
    def __repr__(self):
        return "Chart Player 1"

    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules) -> Literal["hit", "stand", "double", "surrender"]:
        return map_result_char(BASIC_MATRIX[hand.best_total - 4][get_dealer_index(card_val = dealer_up.rank)])

    def decide_bet_amount(self, curr_bet_unit: int, shoe_length: int) -> int:
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
    def __init__(self, bankroll=1000):
        super().__init__(bankroll)
        self.running_count: int = 0

    def __repr__(self):
        return "Running Count High Low Player"
    
    def _update_running_count(self, card: Union[Card, str]) -> None:
        if isinstance(card, str):
            rank = card
        else:
            rank = card.rank
        if rank in ["2", "3", "4", "5", "6"]:
            self.running_count += 1
        elif rank in ["10", "J", "Q", "K", "A"]:
            self.running_count -= 1

    def _reset_running_count(self):
        self.running_count = 0
    
    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules) -> Literal["hit", "stand", "double", "surrender"]:
        if hand.is_soft:
            return map_result_char(SOFT_MATRIX[hand.best_total - 13][get_dealer_index(card_val = dealer_up.rank)])
        else:
            return map_result_char(HARD_MATRIX[hand.best_total - 4][get_dealer_index(card_val = dealer_up.rank)])

    def decide_bet_amount(self, curr_bet_unit: int, shoe_length: int) -> int:
        true_count = self.running_count / max((shoe_length / 52), 1)
        return max(int(max(1, true_count) * curr_bet_unit), curr_bet_unit)
    

class QLearningPlayer(Player):
    def __init__(self, bankroll: int = 1000, 
                 learning_rate: float = 0.1,
                 discount_factor: float = 0.95, 
                 epsilon: float = 0.1,
                 training_mode: bool = True):
        super().__init__(bankroll)
        
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.training_mode = training_mode
        
        self.q_table = {}
        
        self.current_episode = []

    def _get_state(self, hand: Hand, dealer_up: Card) -> tuple:
        player_total = hand.best_total
        dealer_value = dealer_up.hard_value
        has_usable_ace = hand.is_soft
        
        return (player_total, dealer_value, has_usable_ace)
    
    def _get_q_value(self, state: tuple, action: str) -> float:
        if (state, action) not in self.q_table:
            if action == "surrender":
                return -0.5
            else:
                return -0.1
        return self.q_table[(state, action)]
    
    def decide_move(self, hand: Hand, dealer_up: Card, rules: HouseRules) -> Literal["hit", "stand", "double", "surrender"]:
        state = self._get_state(hand, dealer_up)
        
        valid_actions = ["hit", "stand"]
        
        if len(hand.cards) == 2:
            valid_actions.append("double")
            if rules.surrender != "none":
                valid_actions.append("surrender")
        
        if self.training_mode and random.random() < self.epsilon:
            action = random.choice(valid_actions)
        else:
            q_values = {act: self._get_q_value(state, act) for act in valid_actions}
            action = max(q_values, key=q_values.get)
        
        if self.training_mode:
            self.current_episode.append({
                'state': state,
                'action': action
            })
        
        return action
    
    def decide_bet_amount(self, curr_bet_unit: int, shoe_length: int) -> int:
        return curr_bet_unit
    
    def learn_from_hand(self, outcome: str):
        if not self.training_mode or not self.current_episode:
            return
        
        reward_map = {
            'win': 1.0,
            'loss': -1.0,
            'push': 0.0,
            'blackjack': 1.5,
            'surr_loss': -0.5,
            'broke': -10.0
        }
        reward = reward_map.get(outcome, 0.0)
        
        num_decisions = len(self.current_episode)
        
        for i in range(num_decisions - 1, -1, -1):
            decision = self.current_episode[i]
            state = decision['state']
            action = decision['action']
            
            current_q = self._get_q_value(state, action)
            
            if i == num_decisions - 1:
                max_future_q = 0.0
            else:
                next_state = self.current_episode[i + 1]['state']
                max_future_q = max(
                    self._get_q_value(next_state, 'hit'),
                    self._get_q_value(next_state, 'stand')
                )
            
            new_q = current_q + self.learning_rate * (
                reward + self.discount_factor * max_future_q - current_q
            )
            
            self.q_table[(state, action)] = new_q
        
        self.current_episode = []

    def save_model(self, filepath: str):
        model_data = {
            'q_table': self.q_table,
            'learning_rate': self.learning_rate,
            'discount_factor': self.discount_factor
        }
    
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✓ Model saved: {len(self.q_table)} states learned")

    def load_model(self, filepath: str):
        if not os.path.exists(filepath):
            print(f"⚠ Model file not found: {filepath}")
            return
        
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.q_table = model_data['q_table']
        print(f"✓ Model loaded: {len(self.q_table)} states")

    def __repr__(self):
        mode = "Training" if self.training_mode else "Playing"
        return f"Q-Learning AI ({mode})"