import config

# Sum up all key distances and key efforts
def calculate_value(layout):
    value = 0
    for i in range(config.KEY_COUNT):
        frequency = config.frequencies.get(layout[i], 0)
        value += config.key_distances[i] * frequency * config.WEIGHT_DISTANCE
        value += config.key_distances[i] * frequency * config.WEIGHT_EFFORT
        value += calculate_bigram(layout) * config.WEIGHT_BIGRAM
    return value

# Calculate bigram value
def calculate_bigram(layout):
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



