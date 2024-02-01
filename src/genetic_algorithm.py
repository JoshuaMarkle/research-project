import random
import config
from keyboard_layout import calculate_value, crossover, mutate_layout

def optimize_keyboard_layout():
    random.seed()

    keyboards = [config.qwerty_layout[:] for _ in range(config.NUM_KEYBOARDS)]
    best_value = float("inf")
    best_keyboard = keyboards[0][:]

    print(f"Generation 0: Best Keyboard ({calculate_value(config.qwerty_layout)}): {''.join(config.qwerty_layout)}")

    for generation in range(1, config.NUM_GENERATIONS + 1):
        for i in range(config.NUM_KEYBOARDS):
            if i > 0:
                parent_index = random.randint(0, config.NUM_KEYBOARDS - 1)
                keyboards[i] = crossover(best_keyboard, keyboards[parent_index])
                keyboards[i] = mutate_layout(keyboards[i])

            value = calculate_value(keyboards[i])

            if value < best_value:
                best_value = value
                best_keyboard = keyboards[i][:]

        print(f"Generation {generation}, Best Keyboard ({best_value}): {''.join(best_keyboard)}")

    print("\nFinal Best Keyboard Layout:")
    for i, key in enumerate(best_keyboard, 1):
        print(key, end=" ")
        if i % 10 == 0:
            print()
    print()


if __name__ == "__main__":
    config.load_frequencies("data/quotes.txt")
    optimize_keyboard_layout()
