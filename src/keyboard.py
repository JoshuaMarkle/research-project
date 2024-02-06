import random
import config

# Sum up all key distances and key efforts
def calculate_value(layout):
    value = 0
    for i in range(config.KEY_COUNT):
        frequency = config.frequencies.get(layout[i], 0)
        value += config.key_distances[i] * frequency * config.WEIGHT_DISTANCE
        value += config.key_distances[i] * frequency * config.WEIGHT_EFFORT
        value += calculate_bigram_badness(layout) * config.WEIGHT_BIGRAM
    return value


def calculate_bigram_badness(layout):
    badness = 0
    
    for direction_group in config.key_directions:
        substring = ''.join(layout[i] for i in direction_group)
        # print("Constructed Substring:", substring)
        
        # Check for good bigrams
        for bigram in config.bigrams.keys():
            i = 0
            while i < len(substring) - 1:
                first_char_index = substring.find(bigram[0], i)
                if first_char_index != -1:
                    second_char_index = substring.find(bigram[1], first_char_index + 1)
                    if second_char_index != -1:
                        # print("found", bigram)
                        # Decrease badness based on bigram frequency
                        badness -= config.bigrams[bigram]
                        i = second_char_index + 1
                        continue  # Continue searching for more occurrences of the bigram
                i += 1

        # Check for bad/reversed bigrams
        for bigram in config.bigrams.keys():
            reversed_bigram = bigram[::-1]
            i = 0
            while i < len(substring) - 1:
                first_char_index = substring.find(reversed_bigram[0], i)
                if first_char_index != -1:
                    second_char_index = substring.find(reversed_bigram[1], first_char_index + 1)
                    if second_char_index != -1:
                        # print("bad found", reversed_bigram)
                        # Increase badness based on bigram frequency
                        badness += config.bigrams[bigram]  # Use the frequency of the original bigram
                        i = second_char_index + 1
                        continue  # Continue searching for more occurrences of the bigram
                i += 1
    
    return badness

# Switch two random keys
def mutate_layout(layout):
    layout = list(layout)
    for _ in range(random.randint(1, config.MAX_MUTATIONS)):
        index1, index2 = random.sample(range(len(layout)), 2)
        layout[index1], layout[index2] = layout[index2], layout[index1]
    return "".join(layout)

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
