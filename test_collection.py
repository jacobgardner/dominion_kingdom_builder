import dominion
import unittest


class TestDominion(unittest.TestCase):

    def setUp(self):
        self.card_data = {'Sets': [
            dict(name='SetA', cards=[dict(
                name='Card1'
                )]),
            dict(name='SetB', cards=[dict(
                name='Card2'
                )])
        ]}

        self.example_card = dict(name='Card1', set='SetA', type='Action')

        self.preflattened_cards = {
            'Card1': self.example_card,
            'Card2': dict(name='Card2', set='SetB', type=['Action', 'Attack'])
        }

    def test_yaml(self):
        cards = dominion.load_cards()

        assert len(cards)
        self.assertIn('Sets', cards)
        self.assertNotIn('test_yaml', cards)

        cards = dominion.load_cards('test_yaml.yml')

        self.assertIn('test_yaml', cards)

    def test_flattening(self):
        flattened = dominion.flatten_cards(self.card_data)

        self.assertGreater(len(flattened), 0)
        self.assertEquals(flattened[0]['set'], 'SetA')

        self.card_data['Sets'][0]['name'] = 'SetC'

        flattened = dominion.flatten_cards(self.card_data)
        self.assertEquals(flattened[0]['set'], 'SetC')

        cards = dominion.load_cards('test_deck.yml')
        flattened = dominion.flatten_cards(cards)

        self.assertEquals(flattened[1]['set'], 'FileSetB')


class TestCollection(unittest.TestCase):
    def test_classVersion(self):
        collection = dominion.Collection('test_deck.yml')

        assert len(collection.card_tree)
        self.assertIn('Sets', collection.card_tree)
        self.assertNotIn('test_yaml', collection.card_tree)
        self.assertEquals(collection.cards, {
            'FileCard1': dict(name='FileCard1', set='FileSetA', type='Action'),
            'FileCard2': dict(name='FileCard2', set='FileSetB',
                              type=['Action', 'Attack']),
            'FileCard3': dict(name='FileCard3', set='FileSetD', type='Unique')
            })

    def test_class_add(self):
        collection = dominion.Collection('test_deck_2.yml')
        self.assertEquals(collection.cards, {
            'FileCard1': dict(name='FileCard1', set='FileSetA', type='Action'),
            'FileCard2': dict(name='FileCard2', set='FileSetC', type='Action')
            })

        self.assertIn('Action', collection.sorted_cards)
        self.assertEquals(collection.sorted_cards['Action'], [
            dict(name='FileCard1', set='FileSetA', type='Action'),
            dict(name='FileCard2', set='FileSetC', type='Action'),

        ])

        collection = dominion.Collection('test_deck.yml')
        self.assertEquals(collection.sorted_cards['Action'], [
            dict(name='FileCard1', set='FileSetA', type='Action'),
            dict(name='FileCard2', set='FileSetB', type=['Action', 'Attack']),
        ])

        self.assertEquals(collection.sorted_cards['Unique'], [
            dict(name='FileCard3', set='FileSetD', type='Unique')
        ])

        self.assertIn('Attack', collection.sorted_cards)

    def test_card_remove(self):
        collection = dominion.Collection('test_deck.yml')

        collection.remove_card('FileCard3')

        self.assertEquals(collection.sorted_cards['Unique'], [])
        self.assertNotIn('FileCard3', collection.cards)

        collection = dominion.Collection('test_deck.yml')

        collection.remove_card('FileCard1')

        self.assertNotEquals(collection.sorted_cards['Unique'], [])
        self.assertIn('FileCard3', collection.cards)

        collection.remove_card('FileCard2')
