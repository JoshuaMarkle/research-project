import random
import config

def calculate_value(layout):
    total_distance = sum(config.key_distances[i] * config.frequencies.get(layout[i], 0) for i in range(config.KEY_COUNT))
    total_effort = sum(config.key_efforts[i] * config.frequencies.get(layout[i], 0) for i in range(config.KEY_COUNT))
    return total_distance + total_effort

def mutate_layout(layout):
    for _ in range(random.randint(1, config.MAX_MUTATIONS)):
        index1, index2 = random.sample(range(len(layout)), 2)
        layout[index1], layout[index2] = layout[index2], layout[index1]
    return layout

def crossover(parent1, parent2):
    child = parent1[: len(parent1) // 2]
    for key in parent2:
        if key not in child:
            child.append(key)
    return child
