from src.card import Card, build_shoe
from src.hand import Hand
from src.rules import HouseRules
from typing import List, Literal


class Game:
    def __init__(self, rules: HouseRules, player):
        self.rules = rules
        self.player = player
        self.shoe = build_shoe(num_decks=6)

    def play_round(self, bet_amount: int):
        def round_result(
            result: Literal["win", "loss", "push", "blackjack", "surr_loss", "broke"],
            player_hand: Hand | None,
            dealer_hand: Hand | None,
        ):
            if result == "loss":
                self.player.bankroll -= bet_amount
            elif result == "win":
                self.player.bankroll += bet_amount
            elif result == "blackjack":
                self.player.bankroll += bet_amount * self.rules.blackjack_payout
            elif result == "surr_loss":
                self.player.bankroll -= bet_amount * 0.5
            else:
                pass

            return {
                "outcome": result,
                "player": player_hand,
                "dealer": dealer_hand,
                "bankroll": self.player.bankroll,
            }

        # Check reshuffle
        if (
            len(self.shoe) / (self.rules.num_decks * 52)
            <= self.rules.reshuffle_threshold
        ):
            self.shoe = build_shoe(num_decks=self.rules.num_decks)

        # Check bankruptcy
        if self.player.bankroll < bet_amount:
            return round_result("broke", None, None)

        # --- Deal ---
        player_hand = Hand()
        dealer_hand = Hand()

        player_hand.add(self.shoe.pop())
        dealer_hand.add(self.shoe.pop())
        player_hand.add(self.shoe.pop())
        dealer_hand.add(self.shoe.pop())

        # --- Player turn ---
        if player_hand.is_blackjack and dealer_hand.is_blackjack:
            return round_result("push", player_hand, dealer_hand)
        elif player_hand.is_blackjack:
            return round_result("blackjack", player_hand, dealer_hand)
        elif dealer_hand.is_blackjack:
            return round_result("loss", player_hand, dealer_hand)

        while not player_hand.is_bust:
            move = self.player.decide_move(
                player_hand, dealer_hand.cards[0], self.rules
            )
            if move == "hit" or move == "h":
                player_hand.add(self.shoe.pop())
            elif move == "surrender" or move == "r":
                return round_result("surr_loss", None, None)
            elif move == "double" or move == "d":
                player_hand.add(self.shoe.pop())
                bet_amount *= 2
                break
            elif move == "stand" or move == "s":
                break
            else:
                break  # implement splitting

        if player_hand.is_bust:
            return round_result("loss", player_hand, dealer_hand)

        # --- Dealer turn ---
        while True:
            total = dealer_hand.best_total
            while total < 17 or (
                total == 17 and dealer_hand.is_soft and self.rules.dealer_hits_soft_17
            ):
                dealer_hand.add(self.shoe.pop())
                total = dealer_hand.best_total
            else:
                break

        if dealer_hand.is_bust:
            return round_result("win", player_hand, dealer_hand)

        # --- Compare hands ---
        if player_hand.best_total > dealer_hand.best_total:
            return round_result("win", player_hand, dealer_hand)
        elif player_hand.best_total < dealer_hand.best_total:
            return round_result("loss", player_hand, dealer_hand)
        else:
            return round_result("push", player_hand, dealer_hand)
