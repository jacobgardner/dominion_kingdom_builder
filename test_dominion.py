import dominion
import unittest


class TestDominion(unittest.TestCase):

    def test_yaml(self):
        cards = dominion.load_cards()

        assert len(cards)
        assert cards['Sets']
        with self.assertRaises(KeyError):
            cards['test_yaml']

        cards = dominion.load_cards('test_yaml.yml')

        assert cards['test_yaml']

    def test_flattening(self):
        pass
