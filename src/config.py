import random
import json

# Constants
KEY_COUNT = 30
NUM_KEYBOARDS = 100
NUM_GENERATIONS = 300
MAX_MUTATIONS = 1

# Weights
WEIGHT_DISTANCE = 1
WEIGHT_EFFORT = 1
WEIGHT_BIGRAM = 10

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
        key_directions = data[keyboard_type].get("key_directions", [])
    return layers, key_distances, key_efforts, key_directions

def load_corpus_characteristics(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    character_frequencies = data.get("characters", {})
    bigram_frequencies = data.get("bigrams", {})
    trigram_frequencies = data.get("trigrams", {})

    return character_frequencies, bigram_frequencies, trigram_frequencies

# Load from data files
layers, key_distances, key_efforts, key_directions = load_keyboard_characteristics("../data/keyboard.json", "corne")
frequencies, bigrams, trigrams = load_corpus_characteristics("../data/english.json")

# Set the initial keyboard layout
starting = list(layers[0])
