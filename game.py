from dataclasses import dataclass
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
        # TODO: implement game flow: deal, ask player.decide_move(), dealer play, settle bets
        pass