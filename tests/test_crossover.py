import sys
sys.path.append('../src')

from keyboard import crossover

NEW_LAYOUTS = 1 

# Define color codes
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
ENDC = '\033[0m'  # End color

# Reference layouts
qwerty_layout = "qwertyuiopasdfghjkl;zxcvbnm,.'"
dvorak_layout = "',.pyfgcrlaoeuidhtns;qjkxbmwvz"

# Print qwerty and dvorak layouts with colors
print("QWERTY Layout:          DVORAK Layout:")
for i in range(3):
    for k in range(10):
        print(BLUE + qwerty_layout[i * 10 + k] + ENDC, end=" ")
    print("    ", end="")  # Space between layouts
    for k in range(10):
        print(RED + dvorak_layout[i * 10 + k] + ENDC, end=" ")
    print()

# Generate and print NEW_LAYOUTS new layouts with colors
new_layout = crossover(qwerty_layout, dvorak_layout)  # Generate new layout

# Print the new layout
for layout_number in range(NEW_LAYOUTS):
    print(f"\nNew Layout {layout_number + 1}:")
    for i, key in enumerate(new_layout, start=1):
        if key == qwerty_layout[i-1] and key == dvorak_layout[i-1]:
            print(YELLOW + key + ENDC, end=" ")
        elif key == qwerty_layout[i - 1]:
            print(BLUE + key + ENDC, end=" ")
        elif key == dvorak_layout[i - 1]:
            print(RED + key + ENDC, end=" ")
        else:
            print(key, end=" ")  # White by default
        if i % 10 == 0:
            print()  # Newline every 10 characters
    
    # Test for duplication
    print()
    print("Sorted Set: ", "".join(sorted(set(new_layout))), "\nSorted Child: ", "".join(sorted(new_layout)), sep="")
    print()
