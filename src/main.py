import random
import config
from keyboard import calculate_value, crossover, mutate_layout

def optimization_loop():
    random.seed()

    # Initilization
    keyboards = [config.starting_layout[:] for _ in range(config.NUM_KEYBOARDS)]
    best_value = float("inf")
    best_keyboard = keyboards[0][:]
    prev_best_keyboard = keyboards[0][:]

    print(f"Generation 0 ({calculate_value(config.starting_layout):.2f}): {''.join(config.starting_layout)}")

    # The main loop
    for generation in range(1, config.NUM_GENERATIONS + 1):
        # For each keyboard, crossover and mutate
        for i in range(config.NUM_KEYBOARDS):
            if i > 0:
                # Pick a random parent to crossover with
                rand_index = i
                while rand_index == i:
                    rand_index = random.randint(0, config.NUM_KEYBOARDS - 1)
                keyboards[i] = crossover(best_keyboard, keyboards[rand_index])
                keyboards[i] = mutate_layout(keyboards[i])

            # Calculate the keyboard value and check if it is the new best
            value = calculate_value(keyboards[i])
            if value < best_value:
                best_value = value
                best_keyboard = keyboards[i][:]
            
        # Print that generation only if the best keyboard has changed
        if prev_best_keyboard != best_keyboard:
            print(f"Generation {generation} ({best_value:.2f}): {''.join(best_keyboard)}")
            prev_best_keyboard = best_keyboard

    # Print the best keyboard created
    print("\nFinal Best Keyboard Layout:")
    for i, key in enumerate(best_keyboard, 1):
        print(f"[{key}]", end="")
        if i % 10 == 0:
            print()
    print()

if __name__ == "__main__":
    optimization_loop()
