import sys
sys.path.append('../src')

import config

# Output a general overview of the current config
print("Key Count: ", config.KEY_COUNT)
print("Number of Keyboards: ", config.NUM_KEYBOARDS)
print("Number of Generations: ", config.NUM_GENERATIONS)
print("Maximum Mutations: ", config.MAX_MUTATIONS)
print()

# print("Frequencies: ")
# for i, j in config.frequencies.items():
#     print(f"{i} {j}", end="\t")
# print()

print("Key Distances")
for i, key in enumerate(config.key_distances, 1):
    key = str(key)
    if len(key) <= 1:
        key = "0" + key
    print(f"[{key}]", end="")
    if i % 10 == 0:
        print()
print()

print("Key Efforts")
for i, key in enumerate(config.key_efforts, 1):
    key = str(key)
    if len(key) <= 1:
        key = "0" + key
    print(f"[{key}]", end="")
    if i % 10 == 0:
        print()
