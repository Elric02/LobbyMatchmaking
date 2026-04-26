import random
from faker import Faker
import pprint
import utility


def generate_random_results(nb_players, max_players, nb_rounds):
    '''
    Generate random results for testing purposes.

    :param nb_players: the number of players to generate results for
    :type nb_players: int
    :param max_players: the maximum number of players that can be in a match
    :type max_players: int
    :param nb_rounds: how many rounds to generate
    :type nb_rounds: int
    :return: a dictionary where the keys are round numbers and the values are lists of dictionaries with player, lobby, and position (e.g. {1: [{"player": "Alice", "lobby": 1, "position": 1}, {"player": "Bob", "lobby": 1, "position": 2}, {"player": "Charlie", "lobby": 2, "position": 1}]})
    '''

    if nb_rounds < 1:
        raise ValueError("nb_rounds must be at least 1")

    # Create the list of players
    fake = Faker()
    scores = []
    for _ in range(nb_players):
        name = fake.name()
        scores.append((name, 0)) # Initial score is 0

    results = {}

    for current_round in range(1, nb_rounds+1):
        print("----- ROUND", current_round, "-----")
        groups = utility.matchmaking(current_round, scores, max_players)
        print("LOBBIES:", groups)
        
        round_results = []
        for lobby_nr, group in enumerate(groups):
            random.shuffle(group)
            for position, player in enumerate(group):
                round_results.append({"player": player, "lobby": lobby_nr+1, "position": position+1})
        results[current_round] = round_results

        print("RESULTS:")
        pprint.pp(results[current_round])
        print("SCORES:")
        scores = utility.calculate_score(results, max_players)
        pprint.pp(scores)
    
    return results
