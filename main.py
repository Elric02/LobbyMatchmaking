import pprint
import configparser
import utility
import test


results = test.generate_random_results(11, 4, 3)

gsheets_data = utility.get_google_sheets_data("config_worms.ini", ranges=["Scores!A2:A10"])
print("GSHEETS DATA:")
pprint.pprint(gsheets_data)