from dataclasses import dataclass, field
from typing import List
from src.card import Card


@dataclass(slots=True)
class Hand:
    cards: List[Card] = field(default_factory=list)

    def add(self, card: Card) -> None:
        self.cards.append(card)

    def totals(self) -> List[int]:
        total, aces = 0, 0
        for card in self.cards:
            total += card.hard_value
            if card.rank == "A":
                aces += 1
        totals = [total]
        for _ in range(aces):
            totals.append(totals[-1] - 10)
        return sorted(set(t for t in totals if t > 0), reverse=True)

    @property
    def best_total(self) -> int:
        for total in self.totals():
            if total <= 21:
                return total
        return self.totals()[-1] if self.cards else 0

    @property
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.totals == [21]

    @property
    def is_bust(self) -> bool:
        return self.best_total > 21

    @property
    def is_soft(self) -> bool:
        """True if hand contains an Ace counted as 11."""
        total = sum(card.hard_value for card in self.cards)
        has_ace = any(card.rank == "A" for card in self.cards)
        return total <= 21 and has_ace

    def __repr__(self) -> str:
        return f"Hand: {' '.join(str(card) for card in self.cards)} \nTotal: {self.best_total} "
