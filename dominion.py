import yaml


def load_cards(card_set='dominion_cards.yml'):
    with open(card_set, 'r') as f:
        data = yaml.load(f.read())

    return data
