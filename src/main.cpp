#include<iostream>
#include <vector>

using namespace std;

// Constants and data
const int KEY_COUNT = 30;
const int keyDistances[KEY_COUNT] = {
	11, 11, 11, 11, 13, 17, 11, 11, 11, 11, // Upper row
    0,  0,  0,  0,  10, 10,  0,  0,  0,  0, // Home row
    12, 12, 12, 12, 19, 12, 12, 12, 12, 12  // Lower row
};
const int keyEfforts[KEY_COUNT] = {
	6,  2,  1,  6, 11, 14,  9,  1,  1,  7, // Upper row
    1,  0,  0,  0,  7,  7,  0,  0,  0,  1, // Home row
    7,  8, 10,  6, 10,  4,  2,  5,  5,  3  // Lower row
};

// Function prototypes
int calculateDistance(const vector<char>& layout, const string& word);

int main() {
	std::vector<char> layout = {
		'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
		'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
		'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'
	};

	string testWord = "ghosts";
    cout << "Total distance for '" << testWord << "': " << calculateDistance(layout, testWord) << endl;
	testWord = "asked";
    cout << "Total distance for '" << testWord << "': " << calculateDistance(layout, testWord) << endl;

	return 0;
}

// Return the total finger distance traveled over entire string of letters
int calculateDistance(const vector<char>& layout, const string& word) {
    int totalDistance = 0;
    for (int i = 0; i < word.length() - 1; ++i) {
        // Find the index of the current letter in the layout
        char currentLetter = word[i];
        int currentIndex = -1;
        for (int j = 0; j < layout.size(); ++j) {
            if (layout[j] == currentLetter) {
                currentIndex = j;
				break;
            }
        }
        
        // Calculate and add the distance to the totalDistance
        if (currentIndex != -1) {
            totalDistance += keyDistances[currentIndex];
        } else {
			cout << "Could not find the letter " << currentLetter << " in the layout!" << endl;
		}
    }

    return totalDistance;
}

