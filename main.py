import pprint
import configparser
import utility
import test


def process_round(config_file, round_number):
    '''
    Main function to run the matchmaking algorithm and interact with Google Sheets.

    :param config_file: the path to the configuration file
    :type config_file: str
    :param round_number: the current round number. Use 0 to setup the first round, or a positive integer to process the specified round.
    :type round_number: int
    '''
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    max_players = int(config['PARAMS']['MaxPlayers'])

    # Which ranges do we need in the Sheets
    needed_ranges = [
        f"{config['USERNAMES']['Sheet']}!{config['USERNAMES']['Range']}"
    ]
    gsheets_data = utility.get_google_sheets_data(config, ranges=needed_ranges)

    usernames = gsheets_data[0]
    print("usernames: ", usernames)
    usernames_with_scores = [(username[0], 0) for username in usernames if username] # Initial score is 0

    groups = utility.matchmaking(round_number, usernames_with_scores, max_players)

    to_write = []
    for group in groups:
        for i in range(max_players):
            if i < len(group):
                to_write.append(group[i])
            else:
                to_write.append("") # Pad with empty strings to fill the range
    to_write = [[x] for x in to_write] # Convert to list of lists for Google Sheets API
    needed_ranges = [
        f"{config['GAME1']['UsernamesSheet']}!{config['GAME1']['UsernamesRange']}"
    ]
    print(f"Input to Google Sheets on {needed_ranges[0]}: {to_write}")
    utility.write_google_sheets_data(config, ranges=needed_ranges, values=to_write)


# Test with random values, uncomment to run
#results = test.generate_random_results(11, 4, 3)

process_round("config_worms.ini", 0)