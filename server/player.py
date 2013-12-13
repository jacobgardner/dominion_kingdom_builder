from collections import deque
import random


class CardNotInHand(Exception):
    pass


class Player(object):
    def __init__(self, initial_cards=[]):
        self.hand = []
        self.deck = []
        self.in_play = []
        self.discard_pile = initial_cards
        self.draw(5)

    def cleanup(self):
        # Discard your hand and draw a new hand
        for card in self.hand[:]:
            self.discard(card)

        self.discard_pile.extend(self.in_play)
        self.in_play = []

        self.draw(5)

    def discard(self, card):
        # if card not in self.hand:
        self.hand.remove(card)
        self.discard_pile.append(card)

    def draw(self, card_count=5):
        self.hand.extend(self.reveal(card_count))

    def play(self, card):
        if card not in self.hand:
            raise CardNotInHand('{0} is not in your current hand'.format(
                card))

        self.hand.remove(card)
        self.in_play.append(card)

    def reveal(self, card_count=1):
        revealed = []

        if card_count > len(self.deck):
            revealed = list(self.deck)
            card_count -= len(self.deck)
            random.shuffle(self.discard_pile)

            # Shuffle and make the discard pile the new deck
            self.deck, self.discard_pile = deque(self.discard_pile), []

        try:
            for i in xrange(card_count):
                revealed.append(self.deck.pop())
        except IndexError:
            # If there's nothing left, there's nothing left
            pass

        return revealed


    def __str__(self):
        s = ''
        s += 'hand: ' + str(self.hand) + '\n'
        s += 'discard_pile size: ' + str(len(self.discard_pile)) + '\n'
        s += 'deck size: ' + str(len(self.deck)) + '\n'

        return s

    gold = 0
