import copy


class PlayerStat(object):
    def __init__(self, id, rating, score):
        self.id = id
        self.rating = rating
        self.score = score

    def __repr__(self):
        return 'PlayerStat(id={id}, rating={rating}, score={score})'.format(
            id=self.id, rating=self.rating, score=self.score)


def find_k(rating):
    k_factor = [
        (2100, 32),
        (2400, 24),
        (None, 16)
    ]

    for k_rating, k_value in k_factor:
        try:
            if rating < int(k_rating):
                return k_value
        except TypeError:
            return k_value


def expected_score(playerA_rating, playerB_rating):
    q_a, q_b = (10 ** (float(rating)/400) for rating in
                [playerA_rating, playerB_rating])

    return q_a/(q_a + q_b)


def adjust_rating(rating, expected_score, win, k_value):
    win = float(win)
    return rating + k_value * (win - expected_score)


def game_results(players=[]):
    players = [PlayerStat(*player) for player in players]
    players = sorted(players, key=lambda x: x.score, reverse=True)

    output = copy.copy(players)

    for idx, winner in enumerate(output):

        for o, opponent in enumerate(players[idx + 1:]):
            elo_score = 1 if winner.score > opponent.score else 0.5

            expected = expected_score(winner.rating, opponent.rating)

            k = find_k(winner.rating)/(len(players) - 1)
            rating = adjust_rating(winner.rating, expected, elo_score, k)

            expected = expected_score(opponent.rating, winner.rating)
            k = find_k(opponent.rating)/(len(players) - 1)

            output[idx + 1 + o].rating = adjust_rating(
                opponent.rating, expected, 1 - elo_score, k)
            winner.rating = rating
    return output
