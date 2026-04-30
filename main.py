import pprint
import configparser
import utility
import test


results = test.generate_random_results(11, 4, 3)

gsheets_data = utility.get_google_sheets_data("config_worms.ini", ranges=["Règles et games!F3:F51"])
print("usernames: ", gsheets_data[0])