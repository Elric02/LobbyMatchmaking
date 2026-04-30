import random
import configparser
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



### GOOGLE SHEETS API STUFF ###

def connect_google_sheets():
    '''
    Connect to the Google Sheets API and return the service object (this function is mainly used by other functions in this file).
    
    :return: the service object to interact with the Google Sheets API
    '''
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        return service
    except HttpError as err:
        print("HTTP Error occurred:")
        print(err)


# Retrieve the data from the Google Sheets
# Guide to get started (important to setup the credentials): https://developers.google.com/workspace/sheets/api/quickstart/python
# Basically, if you have the credentials.json file in your main folder and the Google Sheets API is enabled in your Google project, you should be good to go.
def get_google_sheets_data(config, ranges):
    '''
    Retrieve data from the specified Google Sheets range. Note: authentication with Google required, see guide in the comments in the code.
    
    :param config: the configuration object
    :type config: configparser.ConfigParser
    :param ranges: a list containing the ranges to retrieve data from (e.g. ["Scores!A2:A10", "Scores!B2:B10"])
    :type ranges: list(str)
    :return: a list of lists containing the values retrieved from the specified ranges
    '''
    spreadsheet_id = config["GSHEET"]["SheetID"]

    try:
        service = connect_google_sheets()
        # Call the Sheets API
        sheet = service.spreadsheets()
        results = []
        for single_range in ranges:
            result = (
                sheet.values()
                .get(spreadsheetId=spreadsheet_id, range=single_range)
                .execute()
            )
            values = result.get("values", [])
            if not values:
                print("No data found for the following range:", single_range)
            results.append(values)
        return results
    except HttpError as err:
        print("HTTP Error occurred:")
        print(err)


def write_google_sheets_data(config, ranges, values):
    '''
    Write data to the specified Google Sheets range. Note: authentication with Google required, see guide in the comments in the code.
    
    :param config: the configuration object
    :type config: configparser.ConfigParser
    :param ranges: the ranges to write data to (e.g. ["Scores!A2:A10"])
    :type ranges: list(str)
    :param values: a list of lists containing the values to write to the specified ranges (one element per range)
    :type values: list(list(str))
    '''
    spreadsheet_id = config["GSHEET"]["SheetID"]

    try:
        service = connect_google_sheets()
        # Call the Sheets API
        sheet = service.spreadsheets()
        body = {"values": values}
        result = (
            sheet.values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=ranges[0],
                valueInputOption="RAW",
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
    except HttpError as err:
        print("HTTP Error occurred:")
        print(err)



### ALGORITHMS STUFF ###

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

