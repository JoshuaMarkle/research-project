#include "keyboardLayout.h"
#include <iostream>

// Constants and data
const int KEY_COUNT = 30;
const int MAX_MUTATIONS = 100;
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

// Evaluation weights
const int WEIGHT_TOTAL_DISTANCE = 1;
const int WEIGHT_TOTAL_EFFORT = 1;

// Example layout
std::vector<char> qwertyLayout = {
	'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
	'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
	'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?'
};
std::vector<char> dvorakLayout = {
	'\'', ',', '.', 'p', 'y', 'f', 'g', 'c', 'r', 'l',
	'a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's',
	';', 'q', 'j', 'k', 'x', 'b', 'm', 'w', 'v', 'z'
};

// Return the total finger distance traveled over entire text
int calculateValue(const vector<char>& layout) {
    // Load frequencies
	string filename = "data/quotes.txt";
    map<char, double> frequencies;

    ifstream file(filename);
	if (!file) {
        cerr << "Failed to open file: " << filename << endl;
    }

    char key;
    double percentage;

    while (file >> key >> percentage) {
        frequencies[key] = percentage;
		// cout << key << percentage << endl;
    }

	// Debug: Print frequencies map
    // cout << "Frequencies:" << endl;
    // for (const auto& pair : frequencies) {
    //     cout << pair.first << ": " << pair.second << "%" << endl;
    // }

	// Calculate total distance & effort
	int totalDistance = 0;
	int totalEffort = 0;
	for (char key : layout) {
		int keyIndex = find(layout.begin(), layout.end(), key) - layout.begin();
		if (keyIndex < layout.size()) { // Check if the key is found
			totalDistance += keyDistances[keyIndex] * frequencies[key]; // Distance of the key location * the frequency of that key
			totalEffort += keyEfforts[keyIndex] * frequencies[key]; // Effort needed for the key location * the frequency of that key
		}
	}

    return keyboardValue(totalDistance, totalEffort);
}

// Mutate the keyboard layout (1 to MAX_MUTATIONS)
void mutateLayout(vector<char>& layout) {
    int numMutations = rand() % MAX_MUTATIONS + 1;
    for (int i = 0; i < numMutations; ++i) {
        // Randomly select two distinct keys to swap
        int index1 = rand() % layout.size();
        int index2 = rand() % layout.size();
        
        // Ensure distinct keys for swapping
        while (index1 == index2) {
            index2 = rand() % layout.size();
        }
        
        // Swap the keys at index1 and index2
        swap(layout[index1], layout[index2]);
    }
}

// Find keyboard layout objective worth
int keyboardValue(int& totalDistance, int& totalEffort) {
	return WEIGHT_TOTAL_DISTANCE * totalDistance + WEIGHT_TOTAL_EFFORT * totalEffort;
}
