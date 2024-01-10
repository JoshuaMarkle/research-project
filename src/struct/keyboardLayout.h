#ifndef KEYBOARD_LAYOUT_H
#define KEYBOARD_LAYOUT_H

#include <vector>
#include <string>
#include <cctype> // for tolower
#include <map>
#include <fstream>
#include <algorithm>

using namespace std;

// Constants and data
extern const int KEY_COUNT;
extern const int keyDistances[];
extern const int keyEfforts[];
extern vector<char> qwertyLayout;

int calculateDistance(const vector<char>& layout);
void mutateLayout(vector<char>& layout);

#endif // KEYBOARD_LAYOUT_H