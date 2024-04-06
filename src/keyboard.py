import random
import config

# Merge two keyboard layouts
def crossover(parent1, parent2):
    child = [None] * len(parent1)
    possibilities = [[parent1[i], parent2[i]] for i in range(len(parent1))]
    positions = set(range(len(parent1)))
    used = set()

    while positions:
        possibility_index = random.choice(list(positions))
        positions.remove(possibility_index)

        # Filter possibilities to remove already used characters
        possibilities[possibility_index] = [p for p in possibilities[possibility_index] if p not in used]

        # If no possibilities left, continue to next iteration
        if not possibilities[possibility_index]:
            continue

        # If only one possibility left, use it; otherwise, choose randomly
        if len(possibilities[possibility_index]) == 1:
            chosen_key = possibilities[possibility_index][0]
        else:
            chosen_key = random.choice(possibilities[possibility_index])

        # Place chosen key in child layout and mark as used
        child[possibility_index] = chosen_key
        used.add(chosen_key)

    # Create a list of unused characters
    all_chars = set(parent1 + parent2)
    unused_chars = list(all_chars - used)

    # Shuffle the list of unused characters to introduce randomness
    random.shuffle(unused_chars)

    # Fill in any None values in child with unused characters
    for i, char in enumerate(child):
        if char is None:
            # Pop an unused character from the list and place it in the child
            child[i] = unused_chars.pop()

    # Ensure all unused characters are used
    if unused_chars:
        raise ValueError("Not all characters were used, which indicates a logic error.")

    return ''.join(child)

# Switch two random keys
def mutate_layout(layout):
    layout = list(layout)
    for _ in range(random.randint(1, config.MAX_MUTATIONS)):
        index1, index2 = random.sample(range(len(layout)), 2)
        layout[index1], layout[index2] = layout[index2], layout[index1]
    return "".join(layout)
