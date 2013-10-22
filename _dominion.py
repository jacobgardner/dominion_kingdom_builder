import yaml
from collections import namedtuple
import random
import copy

CardRange = namedtuple('CardRange', ['min', 'max'])


def add_card(card, collection, sorted_decks):
    collection = copy.copy(collection)
    collection[card['name']] = card

    types = card['type']
    if isinstance(types, str):
        types = [types]

    for card_type in types:

        if card_type not in sorted_decks:
            sorted_decks[card_type] = {}

        sorted_decks[card_type][card['name']] = card

    return collection, sorted_decks


def remove_card(card_name, collection, sorted_decks):
    '''
    Removes the card *card_name* from *collection* and the *sorted_decks*.

    '''
    collection = copy.copy(collection)
    sorted_decks = copy.copy(sorted_decks)

    del collection[card_name]

    for deck in sorted_decks.itervalues():
        try:
            del deck[card_name]
        except KeyError:
            pass

    return collection, sorted_decks


def prune_deck(deck, deck_size, collection, sorted_decks):
    '''
    Returns a pruned version of *deck*
    '''
    try:
        new_deck = random.sample(deck, deck_size)
    except ValueError:
        new_deck = deck

    readd = set([card['name'] for card in deck]) - set([card['name'] for card
                                                        in new_deck])

    for card_name in readd:
        for card in deck:
            if card['name'] == card_name:
                break
        print 'Pruned', card
        collection, sorted_decks = add_card(card, collection, sorted_decks)

    return deck, collection, sorted_decks


def main(deck_size=10, deck_count=1, card_ranges={}):
    with open('dominion_cards.yml') as f:
        data = yaml.load(f.read())

    cards = {}
    sorted_decks = {}

    # Put the set name into each card (It's only the parent for ease of
    #    organizing sets in YAML)
    # Sort and add the card to the collection
    for card_set in data['Sets']:
        for card in card_set['cards']:
            card['set'] = card_set['name']
            cards, sorted_decks = add_card(card, cards, sorted_decks)

    decks = []

    for d in xrange(deck_count):
        decks.append([])

    for card_type, type_range in card_ranges.iteritems():
        type_range = CardRange(*type_range)
        for deck in decks:
            try:
                type_count = random.randint(type_range.min, type_range.max)
                remove_type = True
            except TypeError:
                type_count = type_range.min
                remove_type = False

            try:
                sample = random.sample(sorted_decks[card_type].values(),
                                       type_count)
            except ValueError:
                sample = sorted_decks[card_type].values()

            for card in sample:
                deck.append(card)
                cards, sorted_decks = remove_card(card['name'], cards,
                                                  sorted_decks)

                deck, cards, sorted_decks = prune_deck(deck, deck_size, cards,
                                                       sorted_decks)

        if remove_type:
            for card in sorted_decks[card_type].values():
                cards, sorted_decks = remove_card(card['name'], cards,
                                                  sorted_decks)

    while 1:
        remaining = [deck for deck in decks if len(deck) < deck_size]

        if not remaining:
            break

        for deck in remaining:
            card = random.choice(cards.values())
            deck.append(card)
            cards, sorted_decks = remove_card(card['name'], cards,
                                              sorted_decks)

    for deck in decks:
        print '------------------'
        print 'Deck'
        print '------------------'
        for card in deck:
            print '{0} - {1}'.format(card['name'], card['type'])
        print ''


if __name__ == '__main__':
    main(deck_count=2, card_ranges=dict(Attack=CardRange(1, None),
                                        Reaction=(1, None),
                                        Victory=(0, 0)))
