import sys
sys.path.append('../src')

from keyboard import calculate_bigram_badness

# Define the keyboard layouts
qwerty_layout = "qwertyuiopasdfghjkl;zxcvbnm,.'"
dvorak_layout = "',.pyfgcrlaoeuidhtns;qjkxbmwvz"
colemak_layout = "qwfpgjluy;arstdhneiozxcvbkm,.'"
bad_layout = "naebcdfghijklmopqrstuvwxyz'.,;"
# Function to test badness calculation for a given layout
def test_layout(layout_name, layout):
    badness_score = calculate_bigram_badness(layout)
    print(f"Badness score for {layout_name}: {badness_score}")

# Test the layouts
test_layout("Qwerty", qwerty_layout)
test_layout("Dvorak", dvorak_layout)
test_layout("Colemak", colemak_layout)
test_layout("Bad", bad_layout)
