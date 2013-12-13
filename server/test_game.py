import unittest

from .game import Game
from .player import CardNotInHand


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(
            players=['mrkill', 'jacob', 'matt'],
            cards=['estate', 'province', 'duchy', 'gold', 'copper', 'silver',
                   'lighthouse', 'island', 'talisman', 'workers-village',
                   'trading-post', 'village', 'navigator', 'throne-room',
                   'outpost', 'wharf'])

    def test_turn(self):
        self.assertEquals(self.game.turn_index, 0)
        self.assertEquals(self.game.player_name, 'mrkill')
        self.assertEquals(self.game.player_index, 0)

        self.game.next()
        self.assertEquals(self.game.turn_index, 1)
        self.assertEquals(self.game.player_name, 'jacob')
        self.assertEquals(self.game.player_index, 1)

        self.game.next()
        self.assertEquals(self.game.turn_index, 2)
        self.assertEquals(self.game.player_name, 'matt')
        self.assertEquals(self.game.player_index, 2)

        self.game.next()
        self.assertEquals(self.game.turn_index, 3)
        self.assertEquals(self.game.player_name, 'mrkill')
        self.assertEquals(self.game.player_index, 0)

    def test_play(self):
        self.game.play(card='copper')
        self.assertEquals(len(self.game.player.hand), 4)

        with self.assertRaises(CardNotInHand):
            self.game.play(card='poop')

        self.assertEquals(self.game.player.gold, 1)

        with self.assertRaises(CardNotInHand):
            self.game.play(card='gold')

        self.assertEquals(self.game.player.gold, 1)
