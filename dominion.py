from collections import defaultdict
import yaml


def load_cards(card_set='dominion_cards.yml'):
    with open(card_set, 'r') as f:
        data = yaml.load(f.read())

    return data


def flatten_cards(sets):
    cards = []

    for set_data in sets['Sets']:
        for card in set_data['cards']:
            card['set'] = set_data['name']
            cards.append(card)

    return cards


class Collection(object):
    def __init__(self, card_set='dominion_cards.yml'):

        self.card_tree = load_cards(card_set)
        self.flattened = flatten_cards(self.card_tree)
        self.cards = {}
        self.sorted_cards = defaultdict(list)

        for card in self.flattened:
            self.add_card(card)

    def add_card(self, card):
        self.cards[card['name']] = card
        if isinstance(card['type'], str):
            self.sorted_cards[card['type']].append(card)
        else:
            for card_type in card['type']:
                self.sorted_cards[card_type].append(card)

    def remove_card(self, card_name):
        card = self.cards[card_name]

        types = card['type']
        if isinstance(types, str):
            types = [types]

        for card_type in types:
            self.sorted_cards[card_type].remove(card)

        del self.cards[card_name]
