class InvalidActivity(Exception):
    pass


class BaseCard(object):
    _gold = 0
    _actions = 0
    _buys = 0
    _cost = 0
    _size = 10
    type = []

    def gold(self, game):
        return self._gold

    def actions(self, game):
        return self._actions

    def buys(self, game):
        return self._buys

    def victory(self, game):
        return self._victory

    def cost(self, game):
        return self._cost

    def size(self, game):
        return self._size

    def play(self, game):
        pass

    def resume(self):
        return False


class AttackCard(BaseCard):
    def resume(self):
        try:
            self.iterator.next()
            return True
        except StopIteration:
            return False


class Copper(BaseCard):
    type = ['Treasure']
    _gold = 1
    _cost = 0
    _size = 60


class Silver(BaseCard):
    type = ['Treasure']
    _gold = 2
    _cost = 3
    _size = 40


class Gold(BaseCard):
    type = ['Treasure']
    _gold = 3
    _cost = 6
    _size = 30


class Estate(BaseCard):
    type = ['Victory']
    _victory = 1
    _cost = 2
    _size = 24


class Duchy(BaseCard):
    type = ['Victory']
    _victory = 3
    _cost = 5
    _size = 12


class Province(BaseCard):
    type = ['Victory']
    _victory = 6
    _cost = 8

    def size(self, game):
        return max(12, 3 * len(game.players))


class Adventurer(BaseCard):
    type = ['Action']
    _cost = 6

    def play(self, game):
        treasures = []
        revealed_cards = []

        while len(treasures) < 2:
            try:
                revealed = game.player.reveal(1)[0]
            except IndexError:
                break

            if 'Treasure' in get(revealed).type:
                treasures.append(revealed)
            else:
                revealed_cards.append(revealed)

        game.player.hand.extend(treasures)
        game.player.discard_pile.extend(revealed_cards)


class Bureaucrat(AttackCard):
    type = ['Action', 'Attack']
    _cost = 4

    def play(self, game):
        self.game = game
        game.player.deck.append('silver')

        self.iterator = self._attack()
        # There will always be a next!
        self.iterator.next()

    def _attack(self):
        for player in self.game.player_turns[1:]:
            self.game.wait_for(player, 'bureaucrat')
            yield

    def respond(self, commands, player):
        if commands[0] == 'select':
            if commands[1] not in VICTORY_CARDS:
                raise InvalidActivity('{0} is not a victory card'.format(
                                      commands[1]))
            self.game.players[player].place_on_top(commands[1])
        elif commands[0] == 'reveal':
            for card in self.game.players[player].hand:
                if card in VICTORY_CARDS:
                    raise InvalidActivity(
                        'You revealed your hand, but you had a {0}.'.format(
                            card))
        else:
            raise InvalidActivity(
                '{0} is an invalid verb in this context.'.format(commands[0]))


class Cellar(BaseCard):
    type = ['Action']

    _actions = 1
    _cost = 2

    def play(self, game):
        self.game = game
        game.wait_for(game.player_name, 'cellar')

    def respond(self, commands, player):
        if commands[0] != 'select':
            raise InvalidActivity(
                'You must use the select command to discard cards.')

        for card in commands[1:]:
            self.game.player.discard(card)

        self.game.player.draw(len(commands) - 1)


class Chancellor(BaseCard):
    type = ['Action']
    _cost = 3
    _gold = 2

    def play(self, game):
        self.game = game
        game.wait_for(game.player_name, 'chancellor')

    def respond(self, commands, player):
        if commands[0] == 'yes':
            self.game.player.discard_pile.extend(self.game.player.deck)
            self.game.player.deck = []
        elif commands[0] != 'no':
            raise InvalidActivity(
                '{0} is not a valid response. Expecting yes or no'.format(
                    commands[0]))


class Chapel(BaseCard):
    type = ['Action']
    _cost = 2

    def play(self, game):
        self.game = game
        game.wait_for(game.player_name, 'chapel')

    def respond(self, commands, player):
        if commands[0] != 'select':
            raise InvalidActivity(
                'You must use the select command to trash cards.')

        if len(commands) > 5:
            raise InvalidActivity(
                'You may only trash up to 4 cards.')

        if len(commands) < 2 or commands[1] == 'None':
            return

        for card in commands[1:]:
            self.game.player.trash(card)
            self.game.trash.append(card)


class CouncilRoom(BaseCard):
    type = ['Action']
    _cost = 5
    _buys = 1

    def play(self, game):
        game.player.draw(4)

        for player in game.player_turns[1:]:
            game.players[player].draw(1)


class Feast(BaseCard):
    type = ['Action']
    _cost = 4

    def play(self, game):
        self.game = game
        game.player.trash('feast', source='play')
        game.wait_for(game.player_name, 'feast')

    def respond(self, commands, player):
        if commands[0] != 'select':
            raise InvalidActivity(
                '{0} is not a valid command. Please use select.'.format(
                    commands[0]))

        card = commands[1]

        if get(card).cost(self.game) <= 5:
            self.game.gain(player, card)
        else:
            raise InvalidActivity('The card you selected is worth more than 5')

Lighthouse = Island = Talisman = WorkersVillage = TradingPost = Copper
Village = Navigator = ThroneRoom = Outpost = Wharf = Copper

CARDS = {
    'estate': Estate,
    'duchy': Duchy,
    'province': Province,
    'copper': Copper,
    'silver': Silver,
    'gold': Gold,
    'adventurer': Adventurer,
    'cellar': Cellar,
    'chancellor': Chancellor,
    'chapel': Chapel,
    'council-room': CouncilRoom,
    'feast': Feast,
    'lighthouse': Lighthouse,
    'island': Island,
    'talisman': Talisman,
    'workers-village': WorkersVillage,
    'trading-post': TradingPost,
    'village': Village,
    'navigator': Navigator,
    'throne-room': ThroneRoom,
    'outpost': Outpost,
    'wharf': Wharf,
    'bureaucrat': Bureaucrat,
}


def card_aggregator(type):
    return [name for name, value in CARDS.iteritems()
            if type in value.type]

VICTORY_CARDS = card_aggregator('Victory')
TREASURE_CARDS = card_aggregator('Treasure')
REACTION_CARDS = card_aggregator('Reaction')
ATTACK_CARDS = card_aggregator('Attack')
DURATION_CARDS = card_aggregator('Duration')


def get(card_name):
    return CARDS[card_name]()
