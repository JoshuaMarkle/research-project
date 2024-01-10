#include "geneticAlgorithm.h"

// Constants for genetic algorithm
const int NUM_KEYBOARDS = 100;
const int MAX_MUTATIONS = 100;
const int NUM_GENERATIONS = 1000;

// Genetic algorithm function
void optimizeKeyboardLayout() {
    srand(static_cast<unsigned>(time(nullptr)));
    
    vector<vector<char>> keyboards(NUM_KEYBOARDS, qwertyLayout);
    int bestValue = std::numeric_limits<int>::max();
    vector<char> bestKeyboard = qwertyLayout;
    vector<char> prevBestKeyboard = qwertyLayout;

	// Initial Output
	cout << "Generation 0: Best Keyboard (" << calculateValue(qwertyLayout) << "): '',.pyfgcrlaoeuidhtns;qjkxbmwvz" << endl;

    for (int generation = 1; generation <= NUM_GENERATIONS; ++generation) {
		// Generate keyboards for this generation
        for (int i = 0; i < NUM_KEYBOARDS; ++i) {
            if (i > 0) {
                keyboards[i] = bestKeyboard; // Make a copy of the best keyboard
                mutateLayout(keyboards[i]);  // Mutate the copied layout
            }
			
            // Calculate value for the current keyboard layout
            int value = calculateValue(keyboards[i]);

            
            // Update the best keyboard if the distance is smaller
            if (value < bestValue) {
                bestValue = value;
                bestKeyboard = keyboards[i];
            }
        }

		// Debug: Output only if keyboard layout has changed
		if (prevBestKeyboard != bestKeyboard) {
			cout << "Generation " << generation << ", Best Keyboard (" << bestValue << "): ";
			for (char key : bestKeyboard) {
				cout << key;
			}
			cout << endl;
			prevBestKeyboard = bestKeyboard;
		}
    }

	// Debug: Post genetic algorithm output keyboard
	cout << endl;
	for (int i = 1; i < KEY_COUNT + 1; i++) {
		cout << bestKeyboard[i-1];
		if (i % 10 == 0) { cout << endl; }
	}
	cout << endl;
}

