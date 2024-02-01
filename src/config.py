# Constants
KEY_COUNT = 30
MAX_MUTATIONS = 100
NUM_KEYBOARDS = 100
NUM_GENERATIONS = 100

key_distances = [
    11,
    11,
    11,
    11,
    13,
    17,
    11,
    11,
    11,
    11,  # Upper row
    0,
    0,
    0,
    0,
    10,
    10,
    0,
    0,
    0,
    0,  # Home row
    12,
    12,
    12,
    12,
    19,
    12,
    12,
    12,
    12,
    12,  # Lower row
]
key_efforts = [
    6,
    2,
    1,
    6,
    11,
    14,
    9,
    1,
    1,
    7,  # Upper row
    1,
    0,
    0,
    0,
    7,
    7,
    0,
    0,
    0,
    1,  # Home row
    7,
    8,
    10,
    6,
    10,
    4,
    2,
    5,
    5,
    3,  # Lower row
]

# Default layouts
qwerty_layout = list("qwertyuiopasdfghjkl;zxcvbnm,./")
dvorak_layout = list("',.pyfgcrlaoeuidhtns;qjkxbmwvz")

# Frequencies (initialized as None, to be loaded later)
frequencies = None


def load_frequencies(file_path):
    global frequencies
    frequencies = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(" ")
            char = (
                " " if parts[0] == "" else parts[0]
            )  # Handle space as the first character
            freq = float(parts[-1])  # Frequency is the last part
            frequencies[char] = freq
