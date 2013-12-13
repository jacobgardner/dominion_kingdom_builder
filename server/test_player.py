import unittest

from .player import Player, CardNotInHand


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(initial_cards=['copper'] * 7 + ['estate'] * 3)

    def test_draw(self):
        self.player.draw(5)
        self.player.draw(5)

        self.assertEquals(len(self.player.hand), 10)

        self.player.discard('copper')

        self.assertEquals(len(self.player.hand), 9)

        self.player.draw(5)

        self.assertEquals(len(self.player.hand), 10)

    def test_hand(self):
        self.assertEquals(len(self.player.hand), 5)

    def test_play(self):
        self.player.play('copper')

        self.assertEquals(len(self.player.hand), 4)

        with self.assertRaises(CardNotInHand):
            self.player.play('poop')

    def test_cleanup(self):
        self.player.cleanup()
        self.assertEquals(len(self.player.hand), 5)
        self.assertEquals(len(self.player.discard_pile), 5)

        self.player.play('copper')

        self.player.cleanup()
        self.assertEquals(len(self.player.hand), 5)
        self.assertEquals(len(self.player.discard_pile), 0)
        self.assertEquals(len(self.player.deck), 5)
