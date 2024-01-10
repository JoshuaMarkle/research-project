#include "geneticAlgorithm.h"

// Constants for genetic algorithm
const int NUM_KEYBOARDS = 2;
const int MAX_MUTATIONS = 100;
const int NUM_GENERATIONS = 100;

// Genetic algorithm function
void optimizeKeyboardLayout() {
    srand(static_cast<unsigned>(time(nullptr)));
    
    vector<vector<char>> keyboards(NUM_KEYBOARDS, qwertyLayout);
    int bestDistance = std::numeric_limits<int>::max();
    vector<char> bestKeyboard = qwertyLayout;

	// Initial Output
	cout << "Generation 0: Best Keyboard (" << calculateDistance(qwertyLayout) << "): qwertyuipasdfghjkl;zxcvbnm,." << endl;

    for (int generation = 1; generation <= NUM_GENERATIONS; ++generation) {
		// Generate keyboards for this generation
        for (int i = 0; i < NUM_KEYBOARDS; ++i) {
            if (i > 0) {
                keyboards[i] = bestKeyboard; // Make a copy of the best keyboard
                mutateLayout(keyboards[i]);  // Mutate the copied layout
            }
			
            // Calculate distance for the current keyboard layout
            int distance = calculateDistance(keyboards[i]);
            
            // Update the best keyboard if the distance is smaller
            if (distance < bestDistance) {
                bestDistance = distance;
                bestKeyboard = keyboards[i];
            }
        }

		// Output the best keyboard from every generation
		cout << "Generation " << generation << ", Best Keyboard (" << bestDistance << "): ";
		for (char key : bestKeyboard) {
			cout << key;
		}
		cout << endl;
    }
}

