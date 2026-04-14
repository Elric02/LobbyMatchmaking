import random

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
    :return: a dictionary where the keys are player names and the values are their total scores (e.g. {"Alice": 100, "Bob": 80, "Charlie": 90})
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
            if round == 1: # Don't take into account which lobby it is if it's the first round
                score = max_players - position + 1
            else:
                score = (max_players - ((position + 1) * lobby)) * round_factors[round - 1]
            scores[player] = scores.get(player, 0) + score
    return scores


players = [
    ("Alice", 100), ("Bob", 150), ("Charlie", 120), ("Dave", 130),
    ("Eve", 110), ("Frank", 140), ("Grace", 160), ("Hector", 125),
    ("Ivy", 135), ("Jack", 145), ("Kira", 155), ("Liam", 115),
    ("Mia", 165), ("Noah", 105), ("Olivia", 170), ("Paul", 95),
    ("Quinn", 175), ("Riley", 90), ("Sofia", 180), ("Tom", 85),
    ("Uma", 185), ("Victor", 80), ("Will", 190), ("Xena", 75),
    ("Yara", 195), ("Zane", 70), ("Ava", 200), ("Ben", 65),
    ("Cody", 205), ("Dana", 60), ("Eden", 210), ("Finn", 55),
    ("Gina", 215), ("Holly", 50), ("Ian", 220), ("June", 45),
    ("Kyle", 225), ("Lara", 40), ("Mona", 230), ("Nate", 35),
    ("Opal", 235), ("Pia", 30), ("Quade", 240), ("Reese", 25),
    ("Sage", 245), ("Tess", 20), ("Uri", 250), ("Vera", 15)
]


results = {
    1: [
        {"player": "Alice", "lobby": 1, "position": 1},
        {"player": "Bob", "lobby": 1, "position": 2},
        {"player": "Charlie", "lobby": 1, "position": 3},
        {"player": "Dave", "lobby": 1, "position": 4},
        {"player": "Eve", "lobby": 1, "position": 5},
        {"player": "Frank", "lobby": 1, "position": 6},
        {"player": "Arthur", "lobby": 1, "position": 7},
        {"player": "Gene", "lobby": 1, "position": 8},
        {"player": "Grace", "lobby": 2, "position": 1},
        {"player": "Hector", "lobby": 2, "position": 2},
        {"player": "Ivy", "lobby": 2, "position": 3},
        {"player": "Jack", "lobby": 2, "position": 4},
        {"player": "Kira", "lobby": 2, "position": 5},
        {"player": "Liam", "lobby": 2, "position": 6},
        {"player": "Xavier", "lobby": 2, "position": 7},
        {"player": "Misha", "lobby": 2, "position": 8},
        {"player": "Mia", "lobby": 3, "position": 1},
        {"player": "Noah", "lobby": 3, "position": 2},
        {"player": "Olivia", "lobby": 3, "position": 3},
        {"player": "Paul", "lobby": 3, "position": 4},
        {"player": "Quinn", "lobby": 3, "position": 5},
        {"player": "Riley", "lobby": 3, "position": 6},
        {"player": "Loulou", "lobby": 3, "position": 7},
        {"player": "Fifi", "lobby": 3, "position": 8}
        ]
}

print(calculate_score(results, 8, [0.5, 1, 1, 0.8, 0.8]))