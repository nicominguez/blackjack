from card import Card, build_shoe
from hand import Hand
from rules import HouseRules
from typing import List, Literal


class Game:
    def __init__(self, rules: HouseRules, player):
        self.rules = rules
        self.player = player
        self.shoe = build_shoe(num_decks=6)

    def play_round(self):
        def round_result(result: Literal["win", "loss", "push", "blackjack"]):
            return {
                "outcome": result, 
                "player": player_hand, 
                "dealer": dealer_hand, 
                "bankroll": self.player.bankroll
                }

        # Check if shoe needs to be reshuffled
        if len(self.shoe) / (self.rules.num_decks*52) <= self.rules.reshuffle_threshold:
            self.shoe = build_shoe(num_decks=self.rules.num_decks)


        # --- Deal ---
        player_hand = Hand()
        dealer_hand = Hand()

        player_hand.add(self.shoe.pop())
        dealer_hand.add(self.shoe.pop())
        player_hand.add(self.shoe.pop())
        dealer_hand.add(self.shoe.pop())

        # --- Player turn ---
        if player_hand.is_blackjack and dealer_hand.is_blackjack:
            return round_result("push")
        elif player_hand.is_blackjack:
            return round_result("blackjack")
        elif dealer_hand.is_blackjack:
            return round_result("loss")

        while not player_hand.is_bust:
            move = self.player.decide_move(
                player_hand, dealer_hand.cards[0], self.rules
            )
            if move == "hit":
                player_hand.add(self.shoe.pop())
            elif move == "stand":
                break
            else:
                break  # implement splitting, doubling, surrendering

        if player_hand.is_bust:
            return round_result("loss")

        # --- Dealer turn ---
        while True:
            total = dealer_hand.best_total
            while total < 17 or (total == 17 and dealer_hand.is_soft and self.rules.dealer_hits_soft_17):
                dealer_hand.add(self.shoe.pop())
                total = dealer_hand.best_total
            else:
                break

        if dealer_hand.is_bust:
            return round_result("win")
        
        # --- Compare hands ---
        if player_hand.best_total > dealer_hand.best_total:
            return round_result("win")
        elif player_hand.best_total < dealer_hand.best_total:
            return round_result("loss")
        else:
            return round_result("push")