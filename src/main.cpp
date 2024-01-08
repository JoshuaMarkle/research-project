#include<iostream>
#include<fstream>
#include<vector>
#include <cstdlib>
#include <ctime>
#include<limits>

using namespace std;

// Constants and data
const int KEY_COUNT = 30;
const int NUM_KEYBOARDS = 100;
const int MAX_MUTATIONS = 100;
const int NUM_GENERATIONS = 10000;
const int NUM_GEN_QUOTES = 100;
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

// Example layout
std::vector<char> qwertyLayout = {
	'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
	'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
	'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?'
};

// Function prototypes
int calculateDistance(const vector<char>& layout, const string& word);
string getRandomQuote();
void optimizeKeyboardLayout();
void mutateLayout(vector<char>& layout);

int main() {
	// Start the genetic algorithm
	optimizeKeyboardLayout();
    return 0;

	// string randQuote = getRandomQuote();
	// cout << "Random quote: " << randQuote << endl;
    // cout << "Total quote dist: " << calculateDistance(layout, randQuote) << endl;
	//
	// return 0;
}

// Return the total finger distance traveled over entire text
int calculateDistance(const vector<char>& layout, const string& text) {
    int totalDistance = 0;
    for (int i = 3; i < text.length() - 2; ++i) { // Ignore starting and ending "quotes" and buggy characters
        // Get the current letter and check for space case (base case)
		char currentLetter = tolower(text[i]);
		if (currentLetter == ' ') {
			continue;
		}

        // Find the index of the current letter in the layout
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
			// Letter debugging
			// cout << "Could not find the letter " << currentLetter << " in the layout!" << endl;
		}
    }

    return totalDistance;
}

// Find a random quote in the JSONL file
string getRandomQuote() {
	string filename = "quotes/quotes.jsonl";
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: Unable to open file '" << filename << "'" << endl;
        return "";
    }

    vector<string> quotes;
    string line;
    while (getline(file, line)) {
        quotes.push_back(line);
    }

    // Seed the random number generator
    srand(static_cast<unsigned>(time(nullptr)));

    // Pick a random quote
    int randomIndex = rand() % quotes.size();
    string randomQuote = quotes[randomIndex];

	// Extract the "quote" part from the JSON object
    size_t quoteStart = randomQuote.find("\"quote\":\"");
    if (quoteStart != string::npos) {
        quoteStart += 9; // Move to the start of the actual quote
        size_t quoteEnd = randomQuote.find("\"", quoteStart);
        if (quoteEnd != string::npos) {
            string quoteText = randomQuote.substr(quoteStart, quoteEnd - quoteStart);
			return quoteText;
        }
    }

    return "";
}

// Genetic algorithm function
void optimizeKeyboardLayout() {
    srand(static_cast<unsigned>(time(nullptr)));
    
    vector<vector<char>> keyboards(NUM_KEYBOARDS, qwertyLayout);
    int bestDistance = std::numeric_limits<int>::max();
    vector<char> bestKeyboard = qwertyLayout;

	// Generate a quote for this generation
	string genQuotes = "";
	for (int q = 0; q < NUM_GEN_QUOTES; ++q) {
		genQuotes += getRandomQuote();
	}

    
    for (int generation = 1; generation <= NUM_GENERATIONS; ++generation) {
		// Generate keyboards for this generation
        for (int i = 0; i < NUM_KEYBOARDS; ++i) {
            if (i > 0) {
                keyboards[i] = bestKeyboard; // Make a copy of the best keyboard
                mutateLayout(keyboards[i]);  // Mutate the copied layout
            }
			
            // Calculate distance for the current keyboard layout
            int distance = calculateDistance(keyboards[i], genQuotes);
            
            // Update the best keyboard if the distance is smaller
            if (distance < bestDistance) {
                bestDistance = distance;
                bestKeyboard = keyboards[i];
            }
        }

		// Output the best keyboard from every generation
		if (generation % 10 == true) {
			cout << "Generation " << generation << ", Best Keyboard (" << bestDistance << "): ";
			for (char key : bestKeyboard) {
				cout << key;
			}
			cout << endl;
		} 
    }
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
