from dataclasses import dataclass, field
from .card import Card


@dataclass
class Hand:
    cards: list[Card] = field(default_factory=list)

    def add(self, card: Card) -> None:
        self.cards.append(card)

    def totals(self) -> list[int]:
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
        return len(self.cards) == 2 and self.totals() == [21]

    @property
    def is_bust(self) -> bool:
        return self.best_total > 21

    @property
    def is_soft(self) -> bool:
        has_ace = any(card.rank == "A" for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == "A")
        if aces == 0:
            return False
        non_aces_sum = sum(card.hard_value for card in self.cards if card.rank != "A")
        base = non_aces_sum + aces * 1
        for k in range(1, aces + 1):
            if base + 10 * k <= 21:
                return True
        return False

    def __repr__(self) -> str:
        return f"Hand: {' '.join(str(card) for card in self.cards)} \nTotal: {self.best_total} "
