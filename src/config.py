import random
import json

# Constants
KEY_COUNT = 30
NUM_KEYBOARDS = 1000
NUM_GENERATIONS = 100
MAX_MUTATIONS = 1

# Default layouts
qwerty = list("qwertyuiopasdfghjkl;zxcvbnm,./")
dvorak = list("',.pyfgcrlaoeuidhtns;qjkxbmwvz")
abcs = "abcdefghijklmnopqrstuvwxyz;',."

def random_layout():
    return "".join(random.sample(abcs, len(abcs)))

def load_frequencies(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        frequencies = json.load(file)
    return frequencies

def load_keyboard_characteristics(file_path, keyboard_type):
    with open(file_path, "r") as file:
        data = json.load(file)
        layers = data[keyboard_type]["layers"]
        key_distances = data[keyboard_type]["key_distances"]
        key_efforts = data[keyboard_type]["key_efforts"]
    return layers, key_distances, key_efforts

# Load from data files
layers, key_distances, key_efforts = load_keyboard_characteristics("../data/keyboard.json", "corne")
frequencies = load_frequencies("../data/english.json")

# Set the initial keyboard layout
starting = list(layers[0])
