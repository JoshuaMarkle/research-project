import json
from collections import Counter

def compile_character_statistics(file_path, output_file, n):
    char_count = Counter()
    bigram_count = Counter()
    trigram_count = Counter()

    # Open and read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            clean_line = ''.join(filter(lambda c: 33 <= ord(c) <= 127, line))  # Consider only ASCII characters
            # Count characters
            char_count.update(clean_line)
            # Count bigrams
            bigram_count.update([clean_line[i:i+2] for i in range(len(clean_line) - 1)])
            # Count trigrams
            trigram_count.update([clean_line[i:i+3] for i in range(len(clean_line) - 2)])

    total_chars = sum(char_count.values())
    total_bigrams = sum(bigram_count.values())
    total_trigrams = sum(trigram_count.values())

    # Write character, bigram, and trigram frequencies to a JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json_data = {
            "characters": {char: (count / total_chars * 100) for char, count in char_count.most_common()},
            "bigrams": {bigram: (count / total_bigrams * 100) for bigram, count in bigram_count.most_common(n)},
            "trigrams": {trigram: (count / total_trigrams * 100) for trigram, count in trigram_count.most_common(n)}
        }
        json.dump(json_data, json_file, indent=4, sort_keys=True)

    print(f"Final file written to {output_file}")

if __name__ == "__main__":
    file_path = "../../data/quotes.txt"
    output_file = "../../data/letters.json"
    n = 10  # Number of most common bigrams and trigrams to include
    compile_character_statistics(file_path, output_file, n)
