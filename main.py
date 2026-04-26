import pprint
import configparser
import utility
import test


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

print(utility.matchmaking(1, players[:14], 6))

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

print(utility.calculate_score(results, 8, [0.5, 1, 1, 0.8, 0.8]))

results = test.generate_random_results(11, 4, 3)

