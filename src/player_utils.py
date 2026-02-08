def map_result_char(c: str) -> str:
    RESULT_MAP = {
        "h": "hit",
        "s": "stand",
        "d": "double",
        "r": "surrender",
    }
    return RESULT_MAP[c]

# Applicable regardless of soft/hard hand.
BASIC_MATRIX = [
    # 2,   3,   4,   5,   6,   7,   8,   9,  10,  'A'
    ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 4
    ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 5
    ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 6
    ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 7
    ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 8
    ["d", "d", "d", "d", "d", "h", "h", "h", "h", "h"],  # 9
    ["d", "d", "d", "d", "d", "h", "h", "h", "h", "h"],  # 10
    ["d", "d", "d", "d", "d", "h", "h", "h", "h", "h"],  # 11
    ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 12
    ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 13
    ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 14
    ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 15
    ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 16
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 17
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 18
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 19
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 20
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 21
]

# When player's hand is not soft (it does not have an ace that counts 11).
HARD_MATRIX = [
    # 2,   3,   4,   5,   6,   7,   8,   9,  10,  'A'
    ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 4
    ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 5
    ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 6
    ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 7
    ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],  # 8
    ["h", "d", "d", "d", "d", "h", "h", "h", "h", "h"],  # 9
    ["d", "d", "d", "d", "d", "d", "d", "d", "h", "h"],  # 10
    ["d", "d", "d", "d", "d", "d", "d", "d", "d", "h"],  # 11
    ["h", "h", "s", "s", "s", "h", "h", "h", "h", "h"],  # 12
    ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 13
    ["s", "s", "s", "s", "s", "h", "h", "h", "h", "h"],  # 14
    ["s", "s", "s", "s", "s", "h", "h", "h", "r", "h"],  # 15
    ["s", "s", "s", "s", "s", "h", "h", "r", "r", "r"],  # 16
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 17
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 18
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 19
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 20
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 21
]

# When player's hand is soft (it has an ace that counts 11).
SOFT_MATRIX = [
    # 2,   3,   4,   5,   6,   7,   8,   9,  10,  'A'
    ["h", "h", "h", "d", "d", "h", "h", "h", "h", "h"],  # 13
    ["h", "h", "h", "d", "d", "h", "h", "h", "h", "h"],  # 14
    ["h", "h", "d", "d", "d", "h", "h", "h", "h", "h"],  # 15
    ["h", "h", "d", "d", "d", "h", "h", "h", "h", "h"],  # 16
    ["h", "d", "d", "d", "d", "h", "h", "h", "h", "h"],  # 17
    ["s", "d", "d", "d", "d", "s", "s", "h", "h", "s"],  # 18
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 19
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 20
    ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s"],  # 21
]


def get_dealer_index(card_val: str) -> int:
    """Returns the index for the dealer's upcard_val. This is the column in a matrix."""
    if card_val == "A":
        return 9
    elif card_val in {"10", "J", "Q", "K"}:
        return 8
    else:
        return int(card_val) - 2