import math
import pprint
import configparser
import utility
import test


def process_round(config_file, round_number, generate_next_round=False, prioritize_host=None, write_results=True):
    '''
    Main function to run the matchmaking algorithm and interact with Google Sheets.

    :param config_file: the path to the configuration file
    :type config_file: str
    :param round_number: the current round number. Use 0 to setup the first round, or a positive integer to process the specified round.
    :type round_number: int
    :param generate_next_round: whether to generate the lobbies for the next round. Ignored for round number 0.
    :type generate_next_round: bool
    :param prioritize_host: the username of the player to prioritize for hosting lobbies. If unspecified, no player is prioritized.
    :type prioritize_host: str
    :return (if write_results is False): a list of lists containing the values that would be written to the specified Google Sheets ranges (one element per range)
    '''
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    max_players = int(config['PARAMS']['MaxPlayers'])

    if round_number == 0:
        needed_ranges = [] # Which ranges do we need in the Sheets
        needed_ranges.append(f"{config['USERNAMES']['Sheet']}!{config['USERNAMES']['Range']}")
        gsheets_data = utility.get_google_sheets_data(config, ranges=needed_ranges)
        usernames = gsheets_data[0]
        #print("usernames:", usernames)
        # Scoring
        scores = [(username[0], 0) for username in usernames if username] # Initial score is 0
        groups = utility.matchmaking(0, scores, max_players)

    else:
        usernames_with_results = {}
        # Process each round until and including round_number
        for current_round in range(1, round_number+1):
            needed_ranges = []
            print("Now processing round", current_round, "out of", round_number)
            needed_ranges.append(f"{config[f'GAME{current_round}']['ScoresSheet']}!{config[f'GAME{current_round}']['ScoresUsernameRange']}")
            needed_ranges.append(f"{config[f'GAME{current_round}']['ScoresSheet']}!{config[f'GAME{current_round}']['ScoresRange']}")
            needed_ranges.append(f"{config[f'GAME{current_round}']['IntermediateResultsSheet']}!{config[f'GAME{current_round}']['IntermediateResultsUsernameRange']}")
            gsheets_data = utility.get_google_sheets_data(config, ranges=needed_ranges)
            usernames = gsheets_data[0]
            #print("usernames:", usernames)
            # Scoring
            results = gsheets_data[1]
            temp_usernames_with_results = []
            for i in range(len(usernames)):
                if len(usernames[i]) > 0:
                    temp_usernames_with_results.append({
                        "player": usernames[i][0],
                        "lobby": math.floor(i / max_players) + 1, # Calculate lobby number based on index and max players
                        "position": float(results[i][0])
                    })
            #print("temp_usernames_with_results:", temp_usernames_with_results)
            usernames_with_results[current_round] = temp_usernames_with_results
            round_factors = config['PARAMS']['GameMultiplicators']
            round_factors = [float(x) for x in config['PARAMS']['GameMultiplicators'].split(",")] if round_factors != "0" else 0
            lobby_factor = float(config['PARAMS']['LobbyMultiplicator'])
        scores = utility.calculate_score(usernames_with_results, max_players, round_factors=round_factors, lobby_factor=lobby_factor)
        groups = utility.matchmaking(round_number, scores, max_players)

    to_write = []
    if round_number > 0:
        # Write intermediate results
        temp_to_write = [] # Add another list for the next range
        for username in gsheets_data[2]:
            if len(username) == 0:
                temp_to_write.append([""])
                continue
            score = next((score[1] for score in scores if score[0] == username[0]), "") # Find the score for the username, default to "" if not found
            temp_to_write.append([score])
        to_write.append(temp_to_write)
    # Write next round lobbies if needed
    if generate_next_round or round_number == 0:
        temp_to_write = [] # Add another list for the next range
        for group in groups:
            # If there is a username to prioritize for hosting, put it at the top of the group
            if prioritize_host:
                if prioritize_host in group:
                    group.remove(prioritize_host)
                    group.insert(0, prioritize_host)
            for i in range(max_players):
                if i < len(group):
                    temp_to_write.append([group[i]])
                else:
                    temp_to_write.append([""]) # Pad with empty strings to fill the range
        to_write.append(temp_to_write)
    if not write_results: # Return the output rather than write it on Google Sheets (used for processing results)
        return to_write
    needed_ranges = []
    if round_number == 0:
        needed_ranges.append(f"{config['GAME1']['UsernamesSheet']}!{config['GAME1']['UsernamesRange']}")
    else:
        needed_ranges.append(f"{config[f'GAME{round_number}']['IntermediateResultsSheet']}!{config[f'GAME{round_number}']['IntermediateResultsRange']}")
        if generate_next_round: # Also need to generate the lobbies for next round
            needed_ranges.append(f"{config[f'GAME{round_number+1}']['UsernamesSheet']}!{config[f'GAME{round_number+1}']['UsernamesRange']}")
    print(f"Input to Google Sheets on {needed_ranges}: {to_write}")
    utility.write_google_sheets_data(config, ranges=needed_ranges, values=to_write)


def process_results(config_file, nb_rounds):
    '''
    Function to process the final results and write the scores in the Google Sheets.

    :param config_file: the path to the configuration file
    :type config_file: str
    :param nb_rounds: the number of rounds to process
    :type nb_rounds: int
    '''
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    print("Now writing final results")
    needed_ranges = [
        f"{config[f'GAME{nb_rounds}']['IntermediateResultsSheet']}!{config[f'GAME{nb_rounds}']['IntermediateResultsUsernameRange']}",
        f"{config[f'GAME{nb_rounds}']['IntermediateResultsSheet']}!{config[f'GAME{nb_rounds}']['IntermediateResultsRange']}"
    ]
    gsheets_data = utility.get_google_sheets_data(config, ranges=needed_ranges)
    names, scores = gsheets_data
    # Pair, filter empties, sort alphabetically by name
    pairs = sorted(
        ((n[0], float(s[0])) for n, s in zip(names, scores) if len(n) > 0),
        key=lambda x: x[0].lower()
    )
    # Unpack back into original format
    sorted_names  = [[name]  for name, _  in pairs]
    sorted_scores = [[score] for _, score in pairs]
    final_results = [sorted_names, sorted_scores]
    needed_ranges = [
        f"{config['RESULTS']['Sheet']}!{config['RESULTS']['UsernamesRange']}",
        f"{config['RESULTS']['Sheet']}!{config['RESULTS']['ResultsRange']}"
    ]
    print(f"Input to Google Sheets on {needed_ranges}: {final_results}")
    utility.write_google_sheets_data(config, ranges=needed_ranges, values=final_results)


# Test with random values, uncomment to run
#results = test.generate_random_results(11, 4, 3)

#process_round("configs/config_worms.ini", round_number=0, prioritize_host="VelNewt")
#process_round("configs/config_worms.ini", round_number=1, generate_next_round=True, prioritize_host="VelNewt")
#process_round("configs/config_worms.ini", round_number=2, generate_next_round=True, prioritize_host="VelNewt")
#process_round("configs/config_worms.ini", round_number=3, generate_next_round=False)
process_results("configs/config_worms.ini", nb_rounds=3)