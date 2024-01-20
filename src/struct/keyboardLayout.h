#ifndef KEYBOARD_LAYOUT_H
#define KEYBOARD_LAYOUT_H

#include <vector>
#include <string>
#include <cctype> // for tolower
#include <map>
#include <fstream>
#include <algorithm>
#include <unordered_set>

using namespace std;

// Constants and data
extern const int KEY_COUNT;
extern const int keyDistances[];
extern const int keyEfforts[];
extern vector<char> qwertyLayout;
extern vector<char> dvorakLayout;

int calculateValue(const vector<char>& layout);
void mutateLayout(vector<char>& layout);
int keyboardValue(int& totalDistance, int& totalEffort);
std::vector<char> crossover(const std::vector<char>& parent1, const std::vector<char>& parent2);

#endif // KEYBOARD_LAYOUT_H
