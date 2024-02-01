import config
from genetic_algorithm import optimize_keyboard_layout

if __name__ == "__main__":
    config.load_frequencies("../data/quotes.txt")
    optimize_keyboard_layout()
