#ifndef GENETIC_ALGORITHM_H
#define GENETIC_ALGORITHM_H

#include "../struct/keyboardLayout.h"
#include <iostream>
#include <vector>
#include <limits>
#include <ctime>

using namespace std;

extern const int NUM_KEYBOARDS;
extern const int MAX_MUTATIONS;
extern const int NUM_GENERATIONS;

void optimizeKeyboardLayout();

#endif // GENETIC_ALGORITHM_H
