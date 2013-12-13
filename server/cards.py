class BaseCard(object):
    _gold = 0
    _actions = 0
    _buys = 0
    _cost = 0
    _size = 0
    type = []
    current_id = 0

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


class Bureaucrat(BaseCard):
    type = ['Action', 'Attack']
    _cost = 4

    def play(self, game):
        game.player.cards.append('silver')

        game.attack('bureaucrat')

    def attack(self, game, action):
        if action == 'reveal hand':
            pass
        elif action == 'reveal moat':
            pass
        elif action.startswith('select '):
            pass

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
}


def get(card_name):
    return CARDS[card_name]()
