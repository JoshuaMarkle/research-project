import json

def compile_character_statistics(file_path, output_file):
    char_count = {}
    total_chars = 0

    # Open and read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for c in line:
                # Consider only ASCII characters
                if 32 <= ord(c) <= 127:
                    char_count[c] = char_count.get(c, 0) + 1
                    total_chars += 1

    # Sort the characters by frequency in descending order
    sorted_char_count = sorted(char_count.items(), key=lambda x: x[1], reverse=True)

    # Write character frequencies to a JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json_data = {char: (count / total_chars * 100) for char, count in sorted_char_count}
        json.dump(json_data, json_file, indent=4, sort_keys=True)

    print(f"Character percentages written to {output_file}")

if __name__ == "__main__":
    file_path = "../../data/quotes.txt"
    output_file = "../../data/letters.json"
    compile_character_statistics(file_path, output_file)
