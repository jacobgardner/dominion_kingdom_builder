from collections import defaultdict, namedtuple
import random
import yaml
import copy

_Constraint = namedtuple('Constraint', ['min', 'max'])


def Constraint(min=0, max=None):
    '''
    If *max* is None, then it is unlimited
    '''
    if max and min > max:
        raise ValueError('min must be less than max')
    return _Constraint(min, max)


def load_cards(card_set='dominion_cards.yml'):
    with open(card_set, 'r') as f:
        data = yaml.load(f.read())

    return data


def flatten_cards(sets):
    cards = []

    for set_data in sets['Sets']:
        for card in set_data['cards']:
            card['set'] = set_data['name']
            cards.append(Card(card))

    return cards


class Card(object):
    def __init__(self, card_data):
        # 1-1 Mapping of dictionary to attributes
        self._attrs = []
        for key, value in card_data.iteritems():
            self._attrs.append(key)
            setattr(self, key, value)

    def __cmp__(self, other):
        for attr in self._attrs:
            if getattr(self, attr, None) != getattr(other, attr, None):
                return 1

        return 0


class Collection(object):
    def __init__(self, card_set='dominion_cards.yml'):

        self.card_tree = load_cards(card_set)
        self.flattened = flatten_cards(self.card_tree)
        self.cards = {}
        self.sorted_cards = defaultdict(list)

        for card in self.flattened:
            self.add(card)

    def add(self, card):
        self.cards[card.name] = card
        if isinstance(card.type, str):
            self.sorted_cards[card.type].append(card)
        else:
            for card_type in card.type:
                self.sorted_cards[card_type].append(card)

    def remove(self, card):
        try:
            card = self.cards[card]
        except KeyError:
            pass

        types = card.type
        if isinstance(types, str):
            types = [types]

        for card_type in types:
            self.sorted_cards[card_type].remove(card)

        del self.cards[card.name]

    def create_decks(self, decks=1, deck_size=10, type_constraints={},
                     set_constraints=None, pinned_cards=[]):
        decks = [Deck(deck_size) for _ in xrange(decks)]

        try:
            for card in pinned_cards:
                d = random.choice(decks)
                d.cards.append(self.cards[card])
                self.remove(card)
        except TypeError:
            for pinned_cards, deck in zip(pinned_cards, decks):
                for card in pinned_cards:
                    deck.cards.append(self.cards[card])
                    self.remove(card)

        try:
            if isinstance(set_constraints, str):
                set_constraints = [set_constraints]

            remove_cards = [card for card in self.cards.itervalues()
                            if card.set not in set_constraints]

            for card in remove_cards:
                self.remove(card)

        except TypeError:
            pass

        for key, type_constraint in type_constraints.iteritems():
            type_constraint = Constraint(*type_constraint)

            try:
                type_count = random.randint(type_constraint.min,
                                            type_constraint.max)
                remove_remaining = True
            except TypeError:
                type_count = type_constraint.min
                remove_remaining = False

            for deck in decks:
                try:
                    sample = random.sample(self.sorted_cards[key], type_count)
                except ValueError:
                    sample = self.sorted_cards[key]

                for card in sample:
                    deck.cards.append(card)
                    self.remove(card)

                pruned_cards = deck.prune()

                for card in pruned_cards:
                    self.add(card)

            if remove_remaining:
                for card in copy.copy(self.sorted_cards[key]):
                    self.remove(card)

        while 1:
            remaining = [deck for deck in decks if len(deck) < deck_size]

            if not remaining:
                break

            for deck in remaining:
                try:
                    card = random.choice(self.cards.values())
                except IndexError:
                    raise ValueError(
                        'Not enough cards with your given parameters')
                deck.cards.append(card)
                self.remove(card)

        return decks


class Deck(object):
    def __init__(self, deck_size=10):
        self.cards = []
        self.deck_size = deck_size

    def prune(self):
        try:
            new_cards = random.sample(self.cards, self.deck_size)
            remaining = set(self.cards) - set(new_cards)
            self.cards = new_cards

            return list(remaining)
        except ValueError:
            return []

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return self.cards.__iter__()
