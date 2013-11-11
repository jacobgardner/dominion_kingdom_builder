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
            cards.append(Deck(card))

    return cards


class Deck(object):
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

    def create_kingdom(self, kingdoms=1, deck_size=10, type_constraints={},
                       set_constraints=None, pinned_cards=[]):
        # Create a kingdom for each count
        kingdoms = [Kingdom(deck_size) for _ in xrange(kingdoms)]

        try:
            # If a single list, then distribute the pinned cards across the
            # kingdoms randomly.
            for card in pinned_cards:
                d = random.choice(kingdoms)
                d.cards.append(self.cards[card])
                self.remove(card)
        except TypeError:
            # If a list of lists, then each list corresponds with a kingdom
            # pile
            for pinned_cards, kingdom in zip(pinned_cards, kingdoms):
                for card in pinned_cards:
                    kingdom.cards.append(self.cards[card])
                    self.remove(card)

        try:
            # Wrap it up
            if isinstance(set_constraints, str):
                set_constraints = [set_constraints]

            # Find the cards that aren't in the desired sets
            remove_cards = [card for card in self.cards.itervalues()
                            if card.set not in set_constraints]

            # Remove those desired sets
            for card in remove_cards:
                self.remove(card)

        except TypeError:
            pass

        # Add card-type restraints to the kingdoms
        for key, type_constraint in type_constraints.iteritems():
            type_constraint = Constraint(*type_constraint)

            for kingdom in kingdoms:
                try:
                    # If there's a max, then randomly choose how many of this
                    # type of card to put in the kingdom.
                    type_count = random.randint(type_constraint.min,
                                                type_constraint.max)
                    remove_remaining = True
                except TypeError:
                    # If there's not a max, just insert the minimum number and
                    # let the remaining algorithm add additional cards
                    type_count = type_constraint.min
                    remove_remaining = False

                try:
                    # Take a random sample of cards of the type
                    sample = random.sample(self.sorted_cards[key], type_count)
                except ValueError:
                    # If there aren't enough of that type of card left, just
                    # take all the remaining cards.
                    sample = self.sorted_cards[key]

                # Add the cards to the kingdom and remove them from the
                # collection
                for card in sample:
                    kingdom.cards.append(card)
                    self.remove(card)

                # Prune the kingdom down to the deck size.
                pruned_cards = kingdom.prune()

                # Re-add the pruned cards (if any) to the collection
                for card in pruned_cards:
                    self.add(card)

            # If there was a max, remove all cards of that type from the
            # collection
            if remove_remaining:
                for card in copy.copy(self.sorted_cards[key]):
                    self.remove(card)

        # At this point, all types with constraints on them have been used
        # Just keep adding random cards until the kingdoms are filled up.
        while 1:
            remaining = [kingdom for kingdom in kingdoms
                         if len(kingdom) < deck_size]

            if not remaining:
                break

            for kingdom in remaining:
                try:
                    card = random.choice(self.cards.values())
                except IndexError:
                    raise ValueError(
                        'Not enough cards with your given parameters')
                kingdom.cards.append(card)
                self.remove(card)

        return kingdoms


class Kingdom(object):
    def __init__(self, deck_cnt=10):
        self.cards = []
        self.deck_cnt = deck_cnt

    def prune(self):
        try:
            new_cards = random.sample(self.cards, self.deck_cnt)
            remaining = set(self.cards) - set(new_cards)
            self.cards = new_cards

            return list(remaining)
        except ValueError:
            return []

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return self.cards.__iter__()

    def display_cards(self, cards, sort_on='name', indent=''):
        cards = sorted(cards, key=lambda x: getattr(x, sort_on))
        s = ''
        for card in cards:
            s = ''.join([s, indent, card.name, ' - ', str(card.cost), '\n'])

        return s

    def pprint(self, sort_on='name', group_by_set=True):
        s = ''

        if group_by_set:
            categorized = defaultdict(list)
            for card in self.cards:
                categorized[card.set].append(card)

            for key, cards in categorized.iteritems():
                s = ''.join([s, key, '\n'])
                s = ''.join([s, '=' * len(key), '\n'])
                s = ''.join([s, self.display_cards(cards, sort_on=sort_on,
                                                   indent='  ')])
        else:
            s = self.display_cards(self.cards, sort_on=sort_on)

        return s

    def __str__(self):
        return self.pprint()


def main():
    collection = Collection('dominion_cards.yml')
    kingdoms = collection.create_kingdom(kingdoms=1)

    for idx, kingdom in enumerate(kingdoms):
        print 'Kingdom {0}'.format(idx + 1)
        print '==========='

        # print kingdom.pprint(sort_on='cost', group_by_set=False)
        print kingdom.pprint(sort_on='name', group_by_set=False)


if __name__ == '__main__':
    main()
