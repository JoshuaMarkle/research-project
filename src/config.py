import json

# Constants
KEY_COUNT = 30
MAX_MUTATIONS = 100
NUM_KEYBOARDS = 100
NUM_GENERATIONS = 100

# Default layouts
qwerty_layout = list("qwertyuiopasdfghjkl;zxcvbnm,./")
dvorak_layout = list("',.pyfgcrlaoeuidhtns;qjkxbmwvz")

def load_frequencies(file_path):
    global frequencies
    frequencies = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(" ")
            char = (" " if parts[0] == "" else parts[0])  # Handle space as the first character
            freq = float(parts[-1])  # Frequency is the last part
            frequencies[char] = freq

def load_keyboard_characteristics(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        key_distances = data['key_distances']
        key_efforts = data['key_efforts']
    return key_distances, key_efforts

# Load from data files
key_distances, key_efforts = load_keyboard_characteristics("../data/keyboard_characteristics.json")
frequencies = load_frequencies("../data/quotes.json")
