import random
import config

# Sum up all key distances and key efforts
def calculate_value(layout):
    value = 0
    for i in range(config.KEY_COUNT):
        frequency = config.frequencies.get(layout[i], 0)
        value += config.key_distances[i] * frequency
        value += config.key_distances[i] * frequency 
    return value

# Switch two random keys
def mutate_layout(layout):
    for _ in range(random.randint(1, config.MAX_MUTATIONS)):
        index1, index2 = random.sample(range(len(layout)), 2)
        layout[index1], layout[index2] = layout[index2], layout[index1]
    return layout

def crossover(parent1, parent2):
    child = [None] * len(parent1)
    possibilities = [[parent1[i], parent2[i]] for i in range(len(parent1))]
    positions = list(range(len(parent1)))

    while positions:
        # Choose a random unfilled position
        possibility_index = random.choice(positions)
        
        # Ensure we are not choosing from an empty list
        if not possibilities[possibility_index]:
            positions.remove(possibility_index)
            continue

        # If only one possibility left, use it; otherwise, choose randomly
        if len(possibilities[possibility_index]) == 1:
            chosen_key = possibilities[possibility_index][0]
        else:
            chosen_key = random.choice(possibilities[possibility_index])

        # Place chosen key in child layout
        child[possibility_index] = chosen_key
        positions.remove(possibility_index)  # Remove this position from further consideration

        # Remove chosen key from all other possibilities to avoid duplicates
        for pos in possibilities:
            if chosen_key in pos:
                pos.remove(chosen_key)

        # If a possibility list becomes empty, fix the remaining character in the child layout
        for i, pos in enumerate(possibilities):
            if len(pos) == 1 and child[i] is None:
                child[i] = pos[0]
                if i in positions:
                    positions.remove(i)

    return ''.join(child)
