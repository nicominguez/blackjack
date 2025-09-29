from dataclasses import dataclass
import random

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


@dataclass(frozen=True, slots=True)
class Card:
    rank: str
    suit: str

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    @property
    def hard_value(self) -> int:
        if self.rank == "A":
            return 11
        if self.rank in {"J", "Q", "K"}:
            return 10
        return int(self.rank)


def build_shoe(num_decks: int = 1) -> list[Card]:
    shoe: list[Card] = [
        Card(rank, suit) for _ in range(num_decks) for suit in SUITS for rank in RANKS
    ]
    random.shuffle(shoe)
    return shoe
