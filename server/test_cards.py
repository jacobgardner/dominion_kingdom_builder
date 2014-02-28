import unittest

from . import cards
from .cards import InvalidActivity
from .parser import Parser
from .game import Game


class TestCards(unittest.TestCase):
    def setUp(self):
        self.game = Game(
            players=['mrkill', 'jacob', 'emily'],
            cards_in_supply=[
                'estate', 'province', 'duchy', 'gold', 'copper', 'silver',
                'lighthouse', 'island', 'talisman', 'workers-village',
                'trading-post', 'village', 'navigator', 'throne-room',
                'outpost', 'wharf'])

        self.p = Parser(self.game)

    def test_aggregator(self):
        self.assertIn('estate', cards.card_aggregator('Victory'))
        self.assertEquals(len(cards.card_aggregator('poop')), 0)

    def test_adventurer(self):
        self.game.player.hand[0] = 'adventurer'
        coppers_0 = sum(1 for card in self.game.player.hand
                        if card == 'copper')

        self.game.phase = 'Action'
        self.p.eval('mrkill', 'play adventurer')

        coppers_1 = sum(1 for card in self.game.player.hand
                        if card == 'copper')

        self.assertEquals(coppers_0 + 2, coppers_1)
        self.assertEquals(self.game.player.gold, 0)

    def test_bureaucrat(self):
        self.game.player.hand[0] = 'bureaucrat'
        self.game.players['jacob'].hand = ['copper'] * 4 + ['estate']
        self.game.players['emily'].hand = ['copper'] * 4 + ['estate']

        self.p.eval('mrkill', 'play bureaucrat')

        self.assertEquals(self.game.pending(), ('jacob', 'bureaucrat'))
        self.p.eval('jacob', 'select estate')

        self.assertEquals(self.game.pending(), ('emily', 'bureaucrat'))
        self.p.eval('emily', 'select estate')

        self.game.player.hand[0] = 'bureaucrat'
        self.game.players['jacob'].hand = ['copper'] * 4 + ['cellar']
        self.game.players['emily'].hand = ['copper'] * 4 + ['estate']

        self.game.player.actions = 1
        self.p.eval('mrkill', 'play bureaucrat')

        self.p.eval('jacob', 'reveal')

        with self.assertRaises(InvalidActivity):
            self.p.eval('emily', 'reveal')

        self.p.eval('emily', 'select estate')

        self.p.eval('mrkill', 'done')

    def test_cellar(self):
        self.game.turn_index = 1
        self.game.players['jacob'].hand = ['copper'] * 4 + ['cellar']
        self.game.players['jacob'].deck.extend(['duchy'] * 5)
        self.p.eval('jacob', 'play cellar')
        self.p.eval('jacob', 'select copper copper copper copper')

        self.assertListEqual(['duchy'] * 4, self.game.player.hand)
        self.assertEqual(self.game.player.actions, 1)

        self.p.eval('jacob', 'done')

        with self.assertRaises(Exception):
            self.p.eval('mrkill', 'play chancellor')

    def test_chancellor(self):
        self.game.turn_index = 2
        self.game.player.hand[0] = 'chancellor'

        self.p.eval('emily', 'play chancellor')

        with self.assertRaises(Exception):
            self.p.eval('emily', 'play copper')

        self.p.eval('emily', 'yes')

        self.assertEquals(self.game.player.gold, 2)
        self.assertEquals(len(self.game.player.deck), 0)
        self.assertEquals(len(self.game.player.discard_pile), 5)

    def test_chapel(self):
        self.game.turn_index = 0
        self.game.player.hand = ['estate'] * 4 + ['chapel']
        self.game.player.deck = ['copper'] * 5

        self.p.eval('mrkill', 'play chapel')
        self.p.eval('mrkill', 'select estate estate estate')

        self.assertListEqual(self.game.player.hand, ['estate'])
        self.assertEquals(len(self.game.player.discard_pile), 0)
        self.assertListEqual(self.game.player.deck, ['copper'] * 5)

    def test_council_room(self):
        self.game.player.deck.extend(['duchy'] * 5)
        self.game.player.hand[0] = 'council-room'
        self.game.players['jacob'].deck[-1] = 'province'
        self.game.players['emily'].deck[-1] = 'colony'

        self.p.eval('mrkill', 'play council-room')

        self.assertIn('province', self.game.players['jacob'].hand)
        self.assertIn('colony', self.game.players['emily'].hand)

        self.assertEquals(self.game.player.hand.count('duchy'), 4)
        self.assertEquals(len(self.game.player.hand), 8)

    def test_feast(self):
        self.game.player.hand[0] = 'feast'

        self.p.eval('mrkill', 'play feast')
        self.p.eval('mrkill', 'select duchy')
