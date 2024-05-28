import random
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config
from algorithm.keyboard import crossover, mutate_layout
from algorithm.value import calculate_value

def optimization_loop(callback):
    random.seed()

    # Initilization
    # keyboards = [config.random_layout()[:] for _ in range(config.NUM_KEYBOARDS)]
    # keyboards = ["".join(config.dvorak)[:] for _ in range(config.NUM_KEYBOARDS)]
    keyboards = ["".join(config.starting)[:] for _ in range(config.NUM_KEYBOARDS)]
    best_value = -float("inf")
    best_keyboard = keyboards[0][:]
    prev_best_keyboard = keyboards[0][:]

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

            # Calculate the keyboard value or check if it is the new best
            value = -calculate_value(keyboards[i])
            if value > best_value:
                best_value = value
                best_keyboard = keyboards[i][:]

        # Print that generation only if the best keyboard has changed
        if prev_best_keyboard != best_keyboard:
            # callback(f"{generation} {best_value} {''.join(best_keyboard)}")
            callback([generation, best_value, best_keyboard])
            prev_best_keyboard = best_keyboard
        time.sleep(config.OPTIMIZATION_THREAD_BREAK_TIME)

    # Print the best keyboard created
    print("\nFinal Best Keyboard Layout:")
    for i, key in enumerate(best_keyboard, 1):
        print(f"[{key}]", end="")
        if i % 10 == 0:
            print()
    print()

# Link to the GUI
# class OptimizationWorker(QThread):
#     update_signal = pyqtSignal(str)
#
#     def run(self):
#         while not self.isInterruptionRequested():
#             optimization_loop(self.update_signal.emit)

print("DVORAK:", -calculate_value("".join(config.dvorak)))
print("COLEMAK:", -calculate_value("".join(config.colemak)))
print("Qwerty:", -calculate_value("".join(config.qwerty)))
print("ABCs:", -calculate_value("".join(config.abcs)))

class OptimizationWorker(QObject):
    update = pyqtSignal(list)
    finished = pyqtSignal()

    def run(self):
        optimization_loop(self.update.emit)
        self.finished.emit()
