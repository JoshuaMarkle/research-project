import random
import json

# Application Settings
DEFAULT_FONT_SIZE = 12
ENABLE_AUTOSAVE = False

# Size
GRID_SIZE = 20
GRID_HEIGHT = 100
GRID_WIDTH = 100
KEY_SIZE = 60

# Colors
COLOR_0 = "#ffffff"
COLOR_1 = "#ff5768"
COLOR_2 = "#ff8558"
COLOR_3 = "#ffb347"
COLOR_4 = "#dab551"
COLOR_5 = "#b4b75b"
COLOR_6 = "#23d18b"
COLOR_7 = "#00cef1"
COLOR_8 = "#55aaff"
COLOR_9 = "#7ca3ff"
COLOR_10 = "#a29bff"
COLOR_DARK_0 = "#d0d0d0"
COLOR_DARK_1 = "#ca2954"
COLOR_DARK_2 = "#e9551e"
COLOR_DARK_3 = "#e3a144"
COLOR_DARK_4 = "#c59b2a"
COLOR_DARK_5 = "#969843"
COLOR_DARK_6 = "#20AB73"
COLOR_DARK_7 = "#04b9d9"
COLOR_DARK_8 = "#4D9BE8"
COLOR_DARK_9 = "#7194E8"
COLOR_DARK_10 = "#928ce4"
COLOR_ALT = "#b0b0b0"
COLOR_SELECTED_BORDER = COLOR_DARK_8

# GUI Toggle
NORMAL_TOGGLE = False
DIFFICULTY_TOGGLE = False
FINGER_TOGGLE = False
FINGER_REST_TOGGLE = False

# --- Optimization Parameters ---

# Constants
OPTIMIZATION_THREAD_BREAK_TIME = 0.01 # Ensure responsive UI (larger num = more repsonsive)
KEY_COUNT = 30
NUM_KEYBOARDS = 100
NUM_GENERATIONS = 10000
MAX_MUTATIONS = 2

# Weights
WEIGHT_DISTANCE = 2
WEIGHT_EFFORT = 2
WEIGHT_BIGRAM = 5

# Default layouts
qwerty = list("qwertyuiopasdfghjkl;zxcvbnm,./")
dvorak = list("',.pyfgcrlaoeuidhtns;qjkxbmwvz")
colemak = list("qwfpgjluy;arstdhneiozxcvbkm,./")
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
        key_fingers = data[keyboard_type]["key_fingers"]
        key_directions = data[keyboard_type].get("key_directions", [])
    return layers, key_distances, key_fingers, key_efforts, key_directions

def load_corpus_characteristics(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    character_frequencies = data.get("characters", {})
    bigram_frequencies = data.get("bigrams", {})
    trigram_frequencies = data.get("trigrams", {})

    return character_frequencies, bigram_frequencies, trigram_frequencies

# Load from data files
layers, key_distances, key_efforts, key_fingers, key_directions = load_keyboard_characteristics("../data/keyboard.json", "standard")
frequencies, bigrams, trigrams = load_corpus_characteristics("../data/english.json")

# Set the initial keyboard layout
starting = list(layers[0])
