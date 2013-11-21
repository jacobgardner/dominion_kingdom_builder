import json
import elo

STARTING_ELO = 1200


def print_elos(elos):
    for player in elos:
        print '{0: ^10}'.format(player),

    print ''

    for score in elos.itervalues():
        print '{0: ^10}'.format(round(score)),

    print ''
    print '----------'


def main(results_file, starting_elo=STARTING_ELO):
    with open(results_file, 'rb') as f:
        games = json.load(f)

    players = {}
    for game in games['games']:

        results = []
        for player in game:
            if player == '_game':
                continue
            results.append((player, players.get(player, starting_elo),
                            game[player]))

        adjusted = elo.game_results(players=results)

        for player in adjusted:
            players[player.id] = player.rating

        try:
            print '{0: ^90}'.format(game['_game'])
        except KeyError:
            pass
        print_elos(players)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('results_file')

    args = parser.parse_args()
    main(args.results_file)
