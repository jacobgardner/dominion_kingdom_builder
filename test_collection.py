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
            'Card1': dominion.Deck(self.example_card),
            'Card2': dominion.Deck(dict(name='Card2', set='SetB',
                                        type=['Action', 'Attack']))
        }

    def test_yaml(self):
        cards = dominion.load_cards()

        self.assertGreater(len(cards), 0)
        self.assertIn('Sets', cards)
        self.assertNotIn('test_yaml', cards)

        cards = dominion.load_cards('test_decks/test_yaml.yml')

        self.assertIn('test_yaml', cards)

    def test_flattening(self):
        flattened = dominion.flatten_cards(self.card_data)

        self.assertGreater(len(flattened), 0)
        self.assertEquals(flattened[0].set, 'SetA')

        self.card_data['Sets'][0]['name'] = 'SetC'

        flattened = dominion.flatten_cards(self.card_data)
        self.assertEquals(flattened[0].set, 'SetC')

        cards = dominion.load_cards('test_decks/test_deck.yml')
        flattened = dominion.flatten_cards(cards)

        self.assertEquals(flattened[1].set, 'FileSetB')


class TestCard(unittest.TestCase):
    def setUp(self):
        self.example_card = dict(name='Card1', set='SetA', type='Action')
        self.example_card2 = dict(name='Card2', set='SetB', type='Duration')

    def test_creation(self):
        card = dominion.Deck(self.example_card)
        self.assertEquals(card.name, 'Card1')
        self.assertEquals(card.set, 'SetA')
        self.assertEquals(card.type, 'Action')

        card = dominion.Deck(self.example_card2)
        self.assertEquals(card.name, 'Card2')
        self.assertEquals(card.set, 'SetB')
        self.assertEquals(card.type, 'Duration')

    def test_compare(self):
        card1 = dominion.Deck(self.example_card)
        card2 = dominion.Deck(self.example_card2)
        card3 = dominion.Deck(self.example_card)

        self.assertNotEquals(card1, card2)
        self.assertEquals(card1, card3)


class TestCollection(unittest.TestCase):
    def test_classVersion(self):
        collection = dominion.Collection('test_decks/test_deck.yml')

        assert len(collection.card_tree)
        self.assertIn('Sets', collection.card_tree)
        self.assertNotIn('test_yaml', collection.card_tree)
        self.assertEquals(collection.cards, {
            'FileCard1': dominion.Deck(dict(name='FileCard1', set='FileSetA',
                                            type='Action')),
            'FileCard2': dominion.Deck(dict(name='FileCard2', set='FileSetB',
                                            type=['Action', 'Attack'])),
            'FileCard3': dominion.Deck(dict(name='FileCard3', set='FileSetD',
                                            type='Unique'))
            })

    def test_card_add(self):
        collection = dominion.Collection('test_decks/test_deck_2.yml')
        self.assertEquals(collection.cards, {
            'FileCard1': dominion.Deck(dict(name='FileCard1', set='FileSetA',
                                            type='Action')),
            'FileCard2': dominion.Deck(dict(name='FileCard2', set='FileSetC',
                                            type='Action'))
            })

        self.assertIn('Action', collection.sorted_cards)
        self.assertEquals(collection.sorted_cards['Action'], [
            dominion.Deck(dict(name='FileCard1', set='FileSetA',
                               type='Action')),
            dominion.Deck(dict(name='FileCard2', set='FileSetC',
                               type='Action')),
        ])

        collection = dominion.Collection('test_decks/test_deck.yml')
        self.assertEquals(collection.sorted_cards['Action'], [
            dominion.Deck(dict(name='FileCard1', set='FileSetA',
                               type='Action')),
            dominion.Deck(dict(name='FileCard2', set='FileSetB',
                               type=['Action', 'Attack'])),
        ])

        self.assertEquals(collection.sorted_cards['Unique'], [
            dominion.Deck(dict(name='FileCard3', set='FileSetD',
                               type='Unique'))
        ])

        self.assertIn('Attack', collection.sorted_cards)

    def test_card_remove(self):
        collection = dominion.Collection('test_decks/test_deck.yml')

        collection.remove('FileCard3')

        self.assertEquals(collection.sorted_cards['Unique'], [])
        self.assertNotIn('FileCard3', collection.cards)

        collection = dominion.Collection('test_decks/test_deck.yml')

        collection.remove('FileCard1')

        self.assertNotEquals(collection.sorted_cards['Unique'], [])
        self.assertIn('FileCard3', collection.cards)

        collection.remove('FileCard2')

    def test_create_decks(self):
        collection = dominion.Collection('test_decks/test_deck_3.yml')
        decks = collection.create_supply()

        self.assertEquals(len(decks), 1)
        self.assertEquals(len(decks[0].cards), 10)

        collection = dominion.Collection('test_decks/test_deck_3.yml')
        decks = collection.create_supply(deck_size=3)
        self.assertEquals(len(decks), 1)
        self.assertEquals(len(decks[0].cards), 3)

        collection = dominion.Collection('test_decks/test_deck_3.yml')
        decks = collection.create_supply(supplies=3)
        self.assertEquals(len(decks), 3)

        for i in xrange(3):
            self.assertEquals(len(decks[i].cards), 10)

        collection = dominion.Collection('test_decks/test_deck_3.yml')
        self.assertEquals(len(collection.cards), 41)
        decks = collection.create_supply(supplies=2)
        self.assertNotEqual(decks[0].cards, decks[1].cards)

        self.assertEquals(len(collection.cards), 21)

        for card in decks[0].cards:
            self.assertNotIn(card, decks[1].cards)

    def test_constraint(self):
        c = dominion.Constraint()
        self.assertEquals(c, (0, None))

        c = dominion.Constraint(1)
        self.assertEquals(c, (1, None))

        c = dominion.Constraint(1, 5)
        self.assertEquals(c, (1, 5))

        with self.assertRaises(ValueError):
            c = dominion.Constraint(5, 1)

    def test_type_constraints(self):
        for _ in xrange(30):
            # Repeat 30 times because random used
            collection = dominion.Collection('test_decks/test_deck_3.yml')
            decks = collection.create_supply(
                type_constraints=dict(Action=(1, None)))

            self.assertEquals(len(decks[0]), 10)
            actions = 0

            for card in decks[0]:
                if 'Action' in card.type:
                    actions += 1

            self.assertGreater(actions, 0)

            collection = dominion.Collection('test_decks/test_deck_3.yml')
            decks = collection.create_supply(
                type_constraints=dict(Action=(1, 2)))

            actions = 0

            for card in decks[0]:
                if 'Action' in card.type:
                    actions += 1

            self.assertGreaterEqual(actions, 1)
            self.assertLessEqual(actions, 2)

            with self.assertRaises(ValueError):
                collection = dominion.Collection('test_decks/test_deck_3.yml')
                decks = collection.create_supply(type_constraints=dict(
                    Action=(1, 2), Unique=(0, 3)))

            collection = dominion.Collection('test_decks/test_deck_3.yml')
            decks = collection.create_supply(type_constraints=dict(
                Action=(6, 6), Unique=(6, 6)))

            self.assertEquals(len(decks[0]), 10)

            collection = dominion.Collection('test_decks/test_deck_3.yml')
            decks = collection.create_supply(supplies=2, type_constraints=dict(
                Action=(6, 6), Unique=(6, 6)))

            self.assertEquals(len(decks[0]), 10)
            self.assertEquals(len(decks[1]), 10)

            uniques = 0
            for card in decks[1]:
                if 'Unique' in card.type:
                    uniques += 1

            self.assertGreater(uniques, 0)

            collection = dominion.Collection('test_decks/test_deck_3.yml')
            decks = collection.create_supply(supplies=3, type_constraints=dict(
                Action=(6, 6), Unique=(6, 6)))

            self.assertEquals(len(decks[0]), 10)
            self.assertEquals(len(decks[1]), 10)
            self.assertEquals(len(decks[2]), 10)

    def test_set_constraints(self):
        for _ in xrange(30):
            collection = dominion.Collection('test_decks/test_deck_3.yml')
            decks = collection.create_supply(set_constraints=[
                'FileSetA', 'FileSetB'])

            for card in decks[0]:
                self.assertIn(card.set, ['FileSetA', 'FileSetB'])

            collection = dominion.Collection('test_decks/test_deck_3.yml')
            decks = collection.create_supply(set_constraints=[
                'FileSetD'])

            for card in decks[0]:
                self.assertEquals(card.set, 'FileSetD')

            collection = dominion.Collection('test_decks/test_deck_3.yml')
            decks = collection.create_supply(set_constraints='FileSetD')

            for card in decks[0]:
                self.assertEquals(card.set, 'FileSetD')

    def test_pinned_cards(self):
        for _ in xrange(30):
            collection = dominion.Collection('test_decks/test_deck_3.yml')
            supplies = collection.create_supply(pinned_cards=['FileCard3',
                                                              'FileCard4'])

            names = [card.name for card in supplies[0]]
            self.assertIn('FileCard3', names)
            self.assertIn('FileCard4', names)

            collection = dominion.Collection('test_decks/test_deck_3.yml')
            supplies = collection.create_supply(supplies=2,
                                                pinned_cards=['FileCard3',
                                                              'FileCard4'])
            names = [card.name for card in supplies[0]]
            names.extend([card.name for card in supplies[1]])
            self.assertIn('FileCard3', names)
            self.assertIn('FileCard4', names)

            collection = dominion.Collection('test_decks/test_deck_3.yml')
            supplies = collection.create_supply(supplies=2,
                                                pinned_cards=[['FileCard3'],
                                                              ['FileCard4']])
            names = [card.name for card in supplies[0]]
            names2 = ([card.name for card in supplies[1]])
            self.assertIn('FileCard3', names)
            self.assertIn('FileCard4', names2)


class TestDeck(unittest.TestCase):
    def test_creation(self):
        supply = dominion.Supply()
        self.assertEquals(supply.cards, [])
        self.assertEquals(supply.deck_cnt, 10)

        supply = dominion.Supply(8)
        self.assertEquals(supply.deck_cnt, 8)

    def test_prune(self):
        collection = dominion.Collection('test_decks/test_deck_3.yml')
        decks = collection.create_supply()

        pruned_cards = decks[0].prune()

        self.assertEquals(pruned_cards, [])

        decks[0].deck_cnt = 8

        pruned_cards = decks[0].prune()

        self.assertEquals(len(pruned_cards), 2)
        self.assertEquals(len(decks[0]), 8)

        for card in pruned_cards:
            self.assertNotIn(card, decks[0])
