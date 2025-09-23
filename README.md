# Blackjack Simulator
Simple blackjack simulator with configurable house rules and player strategies to try to find a way to beat the house.
***
### Rules
This includes the number of decks, dealer hit rules, and payouts.

Current options:
* **HouseRules**: Basic US casino rules.
***
### Players
Makes decision to hit, stand, etc.

Current options:
* **Random Player**: Makes moves randomly.
* **Basic Blackjack Strategy**: Follows the basic strategy chart.
* **Perfect Blackjack Strategy**: Follows the perfect strategy chart.
* **AI Player**: TODO
***
### Files
* **`main.py`**: Runs a single round of the game.
* **`simulation.py`**: Runs multiple rounds to test a strategy over time.
* **`game.py`**: Contains the core logic for a single round of Blackjack.
* **`player.py`**: Defines the `Player` class and its subclasses.
* **`rules.py`**: Sets the rules for the game (e.g., number of decks, payouts).
* **`card.py` & `hand.py`**: These files define the fundamental building blocks of the game: cards and hands.
