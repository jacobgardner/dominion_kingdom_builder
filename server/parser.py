
class InvalidPlayer(Exception):
    pass


class InvalidCommand(Exception):
    pass


class Parser(object):
    def __init__(self, game):
        self.game = game

    def eval(self, player, command):
        # Game maintains state.  This just forwards commands to
        # game struct
        if player not in self.game.players:
            raise InvalidPlayer(
                '{0} is not playing this game'.format(player))

        commands = command.split()

        if commands[0] == 'play':
            self.game.play(commands[1], player=player)
        elif commands[0] == 'done':
            self.game.next()
        elif self.game.wait:
            self.game.respond(commands, player=player)
        else:
            raise InvalidCommand('{0} is not a recognized verb.'.format(
                commands[0]))
