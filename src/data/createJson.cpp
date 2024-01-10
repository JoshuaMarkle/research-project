#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

// The result actually do mirror: https://mathweb.ucsd.edu/~crypto/Projects/FeliksDushtsky/letter-freq-compute.pdf

int main() {
    string filename = "../../data/quotes.txt"; // Specify your input file name here
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return 1;
    }

    map<char, int> charCount;
    long long totalChars = 0;
    char c;

    while (file.get(c)) {
        if (c >= 32) {
            c = tolower(c); // Convert to lowercase
            charCount[c]++;
            totalChars++;
        }
    }

    file.close();

    // Transfer data to a vector for sorting
    vector<pair<char, int>> charVec(charCount.begin(), charCount.end());

    // Sort the vector by frequency
    sort(charVec.begin(), charVec.end(), [](const pair<char, int>& a, const pair<char, int>& b) {
        return a.second > b.second; // Descending order
    });

    // Writing to JSON file
    ofstream jsonFile("characters.json");
    jsonFile << "{" << endl;
    for (const auto& pair : charVec) {
        double percentage = static_cast<double>(pair.second) / totalChars * 100;

        // Handle backslash character
        if (pair.first == '\\') {
            jsonFile << "\t\"\\\\\": " << fixed << setprecision(6) << percentage << "," << endl;
        } else {
            jsonFile << "\t\"" << pair.first << "\": " << fixed << setprecision(6) << percentage << "," << endl;
        }
    }
    jsonFile << "}" << endl;

    jsonFile.close();
    cout << "Character percentages written to characters.json" << endl;

    return 0;
}
