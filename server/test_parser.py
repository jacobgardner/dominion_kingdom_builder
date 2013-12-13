import unittest
from .parser import Parser, InvalidPlayer, InvalidCommand
from .game import Game
from .player import CardNotInHand


class TestParser(unittest.TestCase):
    def setUp(self):
        self.game = Game(
            players=['mrkill', 'jacob', 'matt'],
            cards=['estate', 'province', 'duchy', 'gold', 'copper', 'silver',
                   'lighthouse', 'island', 'talisman', 'workers village',
                   'trading post', 'village', 'navigator', 'throne room',
                   'outpost', 'wharf'])

    def test_play(self):
        p = Parser(self.game)

        p.eval('mrkill', 'play copper')

        with self.assertRaises(InvalidPlayer):
            p.eval('patten', 'play gold')

        self.assertEquals(self.game.player.gold, 1)
        self.assertEquals(self.game.players['jacob'].gold, 0)

        with self.assertRaises(InvalidCommand):
            p.eval('mrkill', 'trash copper')

        self.assertEquals(self.game.player.gold, 1)

        with self.assertRaises(CardNotInHand):
            p.eval('mrkill', 'play gold')

        self.assertEquals(self.game.player.gold, 1)

        p.eval('mrkill', 'play copper')

        self.assertEquals(self.game.player.gold, 2)

        self.game.players['mrkill'].hand[0] = 'adventurer'
        coppers_0 = sum(1 for card in self.game.player.hand
                        if card == 'copper')

        p.eval('mrkill', 'play adventurer')

        coppers_1 = sum(1 for card in self.game.player.hand
                        if card == 'copper')

        self.assertEquals(coppers_0 + 2, coppers_1)
        self.assertEquals(self.game.player.gold, 2)
