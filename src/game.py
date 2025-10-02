from src.card import build_shoe
from src.hand import Hand
from src.player import Player
from src.rules import HouseRules
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

    def _check_bankrupcy(self) -> Optional[dict[str, Union[str, Hand, None, float]]]:
        if self.player.bankroll < self.player.decide_bet_amount(self.bet):
            return self._round_result("broke", None, None)

    def _deal(self) -> tuple[Player, Player]:
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add(self.shoe.pop())
        dealer_hand.add(self.shoe.pop())
        player_hand.add(self.shoe.pop())
        dealer_hand.add(self.shoe.pop())
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
                player_hand.add(self.shoe.pop())
            elif move == "surrender":
                return self._round_result("surr_loss", None, None)
            elif move == "double":
                player_hand.add(self.shoe.pop())
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
                dealer_hand.add(self.shoe.pop())
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
