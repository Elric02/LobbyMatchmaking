import pprint
import configparser
import utility
import test


results = test.generate_random_results(11, 4, 3)

utility.get_google_sheets_data("config_worms.ini")