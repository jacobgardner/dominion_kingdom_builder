from .player import Player
from . import cards


class Game(object):
    def __init__(self, players, cards):
        self.player_order = players
        self.players = {}

        for player in players:
            self.players[player] = Player(initial_cards=[
                'estate'] * 3 + ['copper'] * 7)

        self.cards = cards
        self.turn_index = 0

    def next(self):
        self.turn_index += 1

    def play(self, card):
        self.player.play(card)
        card = cards.get(card)

        card.play(self)

        self.player.gold += card.gold(self)


    @property
    def player_name(self):
        return self.player_order[self.turn_index % len(self.players)]

    @property
    def player(self):
        return self.players[self.player_name]

    @property
    def player_index(self):
        return self.turn_index % len(self.players)
