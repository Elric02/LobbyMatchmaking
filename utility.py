import random
import pprint
import configparser


def get_google_sheets_data():
    print("TBD")

def matchmaking(round, players, max_players):
    '''
    Matchmaking function to group players into matches for each round.

    :param round: the current round number (starting at 1)
    :type round: int
    :param players: the names and scores of the players (e.g. [("Alice", 100), ("Bob", 150), ("Charlie", 120)])
    :type players: list(tuple(str, int))
    :param max_players: the maximum number of players that can be in a match
    :type max_players: int
    :return: list of list of str, the matched players for the next round (e.g. [["Alice", "Charlie"], ["Bob", "Dave"]])
    '''

    # For the first round, we randomly shuffle the players and group them into matches of max_players (or closest)
    if round == 1:
        random.shuffle(players)
    # For next rounds, we sort the players by score and group them into matches of max_players (or closest)
    else:
        players.sort(key=lambda x: x[1], reverse=True) # Sort by score descending
    n = len(players)
    g = (n + max_players - 1) // max_players # Number of groups
    base_size = n // g
    extra = n % g
    group_sizes = [base_size + 1] * extra + [base_size] * (g - extra)
    print("Group sizes:", group_sizes)
    groups = []
    start = 0
    for size in group_sizes:
        group = [player[0] for player in players[start:start + size]]
        groups.append(group)
        start += size
    return groups

def calculate_score(results, max_players, round_factors=None):
    '''
    Calculate the total scores for each player based on their results in every previous round.

    :param results: a dictionary where the keys are round numbers and the values are lists of dictionaries with player, lobby, and position (e.g. {1: [{"player": "Alice", "lobby": 1, "position": 1}, {"player": "Bob", "lobby": 1, "position": 2}, {"player": "Charlie", "lobby": 2, "position": 1}]})
    :type results: dict(int, list(dict(str, int)))
    :param max_players: the maximum number of players that can be in a match
    :type max_players: int
    :return: a list of tuples containing the names and scores of the players (e.g. [("Alice", 100), ("Bob", 150), ("Charlie", 120)])
    '''
    scores = {}
    round = 0
    round_factors = [1 for _ in range(len(results))] if round_factors is None else round_factors # Score factor for each round, default is 1 (full score)
    if len(round_factors) < len(results):
        raise ValueError("round_factors must have at least as many elements as there are rounds in results")
    for round_results in results.values():
        round += 1
        for result in round_results:
            player = result["player"]
            lobby = result["lobby"]
            position = result["position"]
            score = (max_players - position) * round_factors[round - 1]
            scores[player] = scores.get(player, 0) + score
    scores = list(scores.items())
    return scores

