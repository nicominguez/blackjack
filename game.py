from card import Card, build_shoe
from hand import Hand
from rules import HouseRules
from player import Player
from typing import List


class Game:
    def __init__(self, rules: HouseRules, player: Player):
        self.rules = rules
        self.player = player
        self.shoe = build_shoe(rules.num_decks)

    def play_round(self):

        # --- Deal ---
        player_hand = Hand()
        dealer_hand = Hand()

        player_hand.add(self.shoe.pop())
        dealer_hand.add(self.shoe.pop())
        player_hand.add(self.shoe.pop())
        dealer_hand.add(self.shoe.pop())

        # --- Player turn ---
        if player_hand.is_blackjack and dealer_hand.is_blackjack:
            return {"outcome": "push", "player": player_hand, "dealer": dealer_hand}
        elif player_hand.is_blackjack:
            return {"outcome": "blackjack", "player": player_hand, "dealer": dealer_hand}
        elif dealer_hand.is_blackjack:
            return {"outcome": "loss", "player": player_hand, "dealer": dealer_hand}

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
            return {"outcome": "loss", "player": player_hand, "dealer": dealer_hand}

        # --- Dealer turn ---
        while True:
            total = dealer_hand.best_total
            while total < 17 or (total == 17 and dealer_hand.is_soft and self.rules.dealer_hits_soft_17):
                dealer_hand.add(self.shoe.pop())
                total = dealer_hand.best_total
            else:
                break

        if dealer_hand.is_bust:
            return {"outcome": "win", "player": player_hand, "dealer": dealer_hand}
        
        # --- Compare hands ---
        if player_hand.best_total > dealer_hand.best_total:
            return {"outcome": "win", "player": player_hand, "dealer": dealer_hand}
        elif player_hand.best_total < dealer_hand.best_total:
            return {"outcome": "loss", "player": player_hand, "dealer": dealer_hand}
        else:
            return {"outcome": "push", "player": player_hand, "dealer": dealer_hand}