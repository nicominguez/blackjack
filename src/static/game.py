from .card import build_shoe
from .hand import Hand
from .player import Player
from .rules import HouseRules
from typing import Literal, Union, Optional


class Game:
    def __init__(self, rules: HouseRules, player: Player, bet: int):
        self.rules: HouseRules = rules
        self.player: Player = player
        self.shoe: list = build_shoe(num_decks=self.rules.num_decks)
        self.bet: int = bet

    def _check_reshuffle(self) -> None:
        if (
            len(self.shoe) / (self.rules.num_decks * 52)
            <= self.rules.reshuffle_threshold
        ):
            self.shoe = build_shoe(num_decks=self.rules.num_decks)
            if hasattr(self.player, '_reset_running_count'):
                self.player._reset_running_count()

    def _check_bankrupcy(self) -> Optional[dict[str, Union[str, Hand, None, float]]]:
        if self.player.bankroll < self.bet:
            return self._round_result("broke", None, None)

    def _deal(self) -> tuple[Hand, Hand]:
        player_hand = Hand()
        dealer_hand = Hand()
        card1 = self.shoe.pop()
        player_hand.add(card1)
        if hasattr(self.player, '_update_running_count'):
            self.player._update_running_count(card1)
        card2 = self.shoe.pop()
        dealer_hand.add(card2)
        if hasattr(self.player, '_update_running_count'):
            self.player._update_running_count(card2)
        card3 = self.shoe.pop()
        player_hand.add(card3)
        if hasattr(self.player, '_update_running_count'):
            self.player._update_running_count(card3)
        card4 = self.shoe.pop()
        dealer_hand.add(card4)
        if hasattr(self.player, '_update_running_count'):
            self.player._update_running_count(card4)
        return (player_hand, dealer_hand)

    def _player_turn(
        self, player_hand: Hand, dealer_hand: Hand
    ) -> Optional[dict[str, Union[str, Hand, None, float]]]:
        if player_hand.is_blackjack and dealer_hand.is_blackjack:
            return self._round_result("push", player_hand, dealer_hand)
        elif player_hand.is_blackjack:
            return self._round_result("blackjack", player_hand, dealer_hand)
        while not player_hand.is_bust:
            move = self.player.decide_move(
                player_hand, dealer_hand.cards[0], self.rules
            )
            if move == "hit":
                card = self.shoe.pop()
                player_hand.add(card)
                if hasattr(self.player, '_update_running_count'):
                    self.player._update_running_count(card)
            elif move == "surrender":
                return self._round_result("surr_loss", None, None)
            elif move == "double":
                card = self.shoe.pop()
                player_hand.add(card)
                if hasattr(self.player, '_update_running_count'):
                    self.player._update_running_count(card)
                self.bet *= 2
                break
            elif move == "stand":
                break
            else:
                break  # TODO implement splitting

        if player_hand.is_bust:
            return self._round_result("loss", player_hand, dealer_hand)

    def _dealer_turn(
        self, player_hand: Hand, dealer_hand: Hand
    ) -> Optional[dict[str, Union[str, Hand, None, float]]]:
        if dealer_hand.is_blackjack:
            return self._round_result("loss", player_hand, dealer_hand)
        while True:
            total = dealer_hand.best_total
            while total < 17 or (
                total == 17 and dealer_hand.is_soft and self.rules.dealer_hits_soft_17
            ):
                card = self.shoe.pop()
                dealer_hand.add(card)
                if hasattr(self.player, '_update_running_count'):
                    self.player._update_running_count(card)
                total = dealer_hand.best_total
            else:
                break
        if dealer_hand.is_bust:
            return self._round_result("win", player_hand, dealer_hand)

    def _compare_hands(
        self, player_hand: Hand, dealer_hand: Hand
    ) -> Optional[dict[str, Union[str, Hand, None, float]]]:
        if player_hand.best_total > dealer_hand.best_total:
            return self._round_result("win", player_hand, dealer_hand)
        elif player_hand.best_total < dealer_hand.best_total:
            return self._round_result("loss", player_hand, dealer_hand)
        else:
            return self._round_result("push", player_hand, dealer_hand)

    def _round_result(
        self,
        result: Literal["win", "loss", "push", "blackjack", "surr_loss", "broke"],
        player_hand: Hand | None,
        dealer_hand: Hand | None,
    ) -> dict[str, Union[str, Hand, None, float]]:
        if result == "loss":
            self.player.bankroll -= self.bet
        elif result == "win":
            self.player.bankroll += self.bet
        elif result == "blackjack":
            self.player.bankroll += self.bet * self.rules.blackjack_payout
        elif result == "surr_loss":
            self.player.bankroll -= self.bet * 0.5
        else:
            pass
        return {
            "outcome": result,
            "player": player_hand,
            "dealer": dealer_hand,
            "bankroll": self.player.bankroll,
        }

    def play_round(self):
        self._check_reshuffle()

        result = self._check_bankrupcy()
        if result:
            return result

        player_hand, dealer_hand = self._deal()

        result = self._player_turn(player_hand, dealer_hand)
        if result: 
            return result
        
        result = self._dealer_turn(player_hand, dealer_hand)
        if result: 
            return result
        
        return self._compare_hands(player_hand, dealer_hand)
