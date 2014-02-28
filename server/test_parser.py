import unittest

from .parser import Parser, InvalidPlayer, InvalidCommand
from .game import Game
from .player import CardNotInHand
from .cards import InvalidActivity


class TestParser(unittest.TestCase):
    def setUp(self):
        self.game = Game(
            players=['mrkill', 'jacob', 'emily'],
            cards_in_supply=[
                'estate', 'province', 'duchy', 'gold', 'copper', 'silver',
                'lighthouse', 'island', 'talisman', 'workers-village',
                'trading-post', 'village', 'navigator', 'throne-room',
                'outpost', 'wharf'])

    def test_play(self):
        p = Parser(self.game)

        p.eval('mrkill', 'play copper')

        with self.assertRaises(InvalidPlayer):
            p.eval('patten', 'play gold')

        self.assertEquals(self.game.player.gold, 1)
        self.assertEquals(self.game.players['jacob'].gold, 0)

        self.game.turn_index = 1
        p.eval('jacob', 'play copper')

        self.assertEquals(self.game.player.gold, 1)
        self.assertEquals(self.game.players['jacob'].gold, 1)

        self.game.turn_index = 0

        with self.assertRaises(InvalidCommand):
            p.eval('mrkill', 'trash copper')

        self.assertEquals(self.game.player.gold, 1)

        with self.assertRaises(CardNotInHand):
            p.eval('mrkill', 'play gold')

        self.assertEquals(self.game.player.gold, 1)

        p.eval('mrkill', 'play copper')

        self.assertEquals(self.game.player.gold, 2)

