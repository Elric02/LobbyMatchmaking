import random

def matchmaking(round, players, max_players):
    '''
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
        groups = []
        for i in range(0, len(players), max_players):
            group = [player[0] for player in players[i:i + max_players]]
            groups.append(group)
        return groups
    

print(matchmaking(1, [("Alice", 100), ("Bob", 150), ("Charlie", 120), ("Dave", 130), ("Eve", 110), ("Frank", 140), ("Grace", 160)], 4))