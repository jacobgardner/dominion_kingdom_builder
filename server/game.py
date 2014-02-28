from .player import Player
from . import cards


class NotYourTurn(Exception):
    pass


class NoRemainingActions(Exception):
    pass


class Game(object):
    def __init__(self, players, cards_in_supply):
        self.player_order = players
        self.players = {}
        self.active_card = None
        self.wait = None
        self.phase = 'Action'
        self.trash = []

        for player in players:
            self.players[player] = Player(initial_cards=[
                'estate'] * 3 + ['copper'] * 7)

        self.cards = cards_in_supply
        self.supply = {}
        for card in cards_in_supply:
            self.supply[card] = cards.get(card).size(self)
        self.turn_index = 0

    def gain(self, player, card):
        pass

    def next(self):
        self.player.cleanup()
        self.turn_index += 1
        self.active_card = None
        self.phase = 'Action'
        self.wait = None

    def pending(self):
        return self.wait

    def play(self, card_name, player=None):
        if not player:
            player = self.player
        else:
            player = self.players[player]

        if not self.wait and player != self.player:
            raise Exception("Please wait your turn.  It is {0}'s turn".format(
                self.player_name))

        if self.wait:
            raise Exception("Waiting for {0} to respond to {1}".format(
                *self.wait))

        card = cards.get(card_name)

        if 'Action' in card.type:
            if player.actions <= 0:
                raise NoRemainingActions('You have run out of actions.')
            elif self.phase != 'Action':
                raise Exception('You are in the treasure phase')
            else:
                self.player.actions -= 1
        elif 'Treasure' in card.type:
            self.phase = 'Treasure'

        player.play(card_name)

        player.gold += card.gold(self)
        player.actions += card.actions(self)

        self.active_card = card

        card.play(self)

    def respond(self, commands, player):
        if player != self.wait[0]:
            raise NotYourTurn('Waiting on {0}'.format(self.wait[0]))

        # If react in player hand is applicable, ask if they wish to play it
        # If it's at this point, it's too late... :(

        self.active_card.respond(commands, player)
        if not self.active_card.resume():
            self.wait = None

    def wait_for(self, player, card):
        # An attack card was likely played.  Get response
        self.wait = (player, card)

    @property
    def player_name(self):
        return self.player_order[self.turn_index % len(self.players)]

    @property
    def player(self):
        return self.players[self.player_name]

    @property
    def player_index(self):
        return self.turn_index % len(self.players)

    @property
    def player_turns(self):
        divider = self.turn_index % len(self.players)
        return self.player_order[divider:] + self.player_order[:divider]
