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

# Merge two keyboard layouts using a cyclic algorithm
def crossover(parent1, parent2):
    # Initialize the child layout
    child = [None] * len(parent1)

    def perform_cycle(start_index, source_parent, target_parent):
        current_index = start_index
        cycle_length = 0
        while cycle_length < config.MAX_CROSSOVER_CYCLES:
            # Copy the key from the source parent to the child
            if child[current_index] is None:
                child[current_index] = source_parent[current_index]
            
            # Find the next key in the target parent that matches the current key in the source parent
            next_key = source_parent[current_index]
            next_index = target_parent.index(next_key)

            cycle_length += 1

            # If the cycle is complete or the next key position is already filled, break
            if next_index == start_index or child[next_index] is not None:
                break
            else:
                current_index = next_index

    unfilled_indices = set(range(len(parent1)))  # Use a set for faster removals
    while unfilled_indices:
        # Select a random start index from the unfilled positions
        start_index = random.choice(list(unfilled_indices))

        # Alternately choose parents to start from for each new cycle
        if len(unfilled_indices) % 2 == 0:
            perform_cycle(start_index, parent1, parent2)
        else:
            perform_cycle(start_index, parent2, parent1)

        # Remove the filled positions from the set of unfilled indices
        unfilled_indices = {i for i in unfilled_indices if child[i] is None}

    return child
