import pprint
import configparser
import utility
import test


def process_round(config_file, round_number, prioritize_host=None):
    '''
    Main function to run the matchmaking algorithm and interact with Google Sheets.

    :param config_file: the path to the configuration file
    :type config_file: str
    :param round_number: the current round number. Use 0 to setup the first round, or a positive integer to process the specified round.
    :type round_number: int
    :param prioritize_host: the username of the player to prioritize for hosting lobbies. If unspecified, no player is prioritized.
    :type prioritize_host: str
    '''
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    max_players = int(config['PARAMS']['MaxPlayers'])

    # Which ranges do we need in the Sheets
    needed_ranges = []
    if round_number == 0:
        needed_ranges.append(f"{config['USERNAMES']['Sheet']}!{config['USERNAMES']['Range']}")
    else:
        needed_ranges.append(f"{config[f'GAME{round_number}']['ScoresSheet']}!{config[f'GAME{round_number}']['ScoresUsernameRange']}")
        needed_ranges.append(f"{config[f'GAME{round_number}']['ScoresSheet']}!{config[f'GAME{round_number}']['ScoresRange']}")
    gsheets_data = utility.get_google_sheets_data(config, ranges=needed_ranges)

    usernames = gsheets_data[0]
    print("usernames: ", usernames)
    if round_number == 0:
        usernames_with_results = [(username[0], 0) for username in usernames if username] # Initial score is 0
    else:
        results = gsheets_data[1]
        usernames_with_results = [(usernames[i][0], float(results[i][0])) for i in range(len(usernames)) if len(usernames[i]) > 0] # Get the results, default to 0 if empty
        print("usernames_with_results: ", usernames_with_results)
    scores = utility.calculate_score(usernames_with_results, max_players)
    print(scores)
    exit()

    groups = utility.matchmaking(round_number, scores, max_players)
    to_write = []
    for group in groups:
        # If there is a username to prioritize for hosting, put it at the top of the group
        if prioritize_host:
            if prioritize_host in group:
                group.remove(prioritize_host)
                group.insert(0, prioritize_host)
        for i in range(max_players):
            if i < len(group):
                to_write.append(group[i])
            else:
                to_write.append("") # Pad with empty strings to fill the range
    to_write = [[x] for x in to_write] # Convert to list of lists for Google Sheets API
    needed_ranges = []
    if round_number == 0:
        needed_ranges.append(f"{config['GAME1']['UsernamesSheet']}!{config['GAME1']['UsernamesRange']}")
    else:
        needed_ranges.append(f"{config[f'GAME{round_number}']['Sheet']}!{config[f'GAME{round_number}']['UsernamesRange']}")
    print(f"Input to Google Sheets on {needed_ranges[0]}: {to_write}")
    utility.write_google_sheets_data(config, ranges=needed_ranges, values=to_write)


# Test with random values, uncomment to run
#results = test.generate_random_results(11, 4, 3)

#process_round("configs/config_worms.ini", 0, prioritize_host="VelNewt")
process_round("configs/config_worms.ini", 1, prioritize_host="VelNewt")