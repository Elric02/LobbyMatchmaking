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

    # Which ranges do we need in the Sheets
    needed_ranges = [
        f"{config['USERNAMES']['Sheet']}!{config['USERNAMES']['Range']}"
    ]
    gsheets_data = utility.get_google_sheets_data(config, ranges=needed_ranges)

    usernames = gsheets_data[0]
    print("usernames: ", usernames)


# Test with random values, uncomment to run
#results = test.generate_random_results(11, 4, 3)

process_round("config_worms.ini", 1)