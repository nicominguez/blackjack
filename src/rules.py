from dataclasses import dataclass


@dataclass(slots=True)
class HouseRules:
    num_decks: int = 6
    dealer_hits_soft_17: bool = False
    blackjack_payout: float = 1.5
    double_after_split: bool = True
    double_allowed: str = "any"
    surrender: str = "none"
    peek_for_blackjack: bool = True
    resplit_aces: bool = False
    hit_split_aces: bool = False
    max_splits: int = 3
    reshuffle_threshold = 0.25  # reshuffle when only 25% of the shoe remains
    continuous_reshuffle = False
