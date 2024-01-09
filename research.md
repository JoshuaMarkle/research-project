# Research on Keyboard Layouts

Objective: Study the efficency of a keyboard layouts and the parameters that make a good keyboard layout

Goal: Create an genetic algorithm that can determine the best (and worst) keyboard layouts

## Entries in the research journal

- Research significance
- Charateristics of a keyborad
  - What are the things that make up a keyboard?
    A keyboard layout is characterized by the way each letter is positioned relative to the other keys. Some arrangements are better than others typically my putting the most commonly typed letters on the home row of the keyboard.
  - How to make a keyboard better?
    There are many factors that make a keboard 'better' and ultimately that is a subjective measure. I want to find a good way to objectively test how to make a keyboard layout efficiency and even practicality in the real world.
  - Parameters for a optimal keyboard layout
    The optimimal keyboard layout will have all of the most commonly typed letters somewhere easy to reach. That is the core characteristic behind if a certain layout is better than another but there are also some smaller details that can impact the typing experience. For example, someone typing normal english will want a different layout than a programmer who writes a lot of code for a living. You can also take into account common letter doubles like 'th' or 'ch' and make them roll inward on the keyboard. The human hand wants to roll keypresses from the pinkys inward to the index fingers. This will make the typing experience much more enjoyable and smooth. Another thing to keep track of is the actual physical keyboard itself. A normal keyboard has all of the keys staggered in such a way that works but is not entirely natural. Its natural for the right hand but really unnatural for the left if you look at the way that the staggering works. The best alternative is to use an ortholinear keyboard where all of the keys are straight up and down. This is much more natural than the normal keyboard stagger but there is even more to improve. You can go further to split the keyboard in half for each hand, curve the physical keyboard to account for each finger length, and add more buttons to the thumb. It turns out that the thumb is pretty dexerious, at least more than the pinky, and can be used to type a bunch of letters at once. Physical keyboards can also have a glove type build where the keys are curved upwards to make the keys on the keyboard easies to reasch such as the Fkeys.
- Popular keyboard layouts
  - Layouts background (Qwerty)
    A short background on Qwerty and why we haven't been able to get rid of it today
  - Qwerty
    The pros and cons of the qwerty keyboard. What does it do good and bad.
  - Dvorak
    The pros and cons of the dvorak keyboard. What does it do good and bad.
  - Colmak
    The pros and cons of the colmak keyboard. What does it do good and bad.
  - Workman
    The pros and cons of the workman keyboard. What does it do good and bad.
  - Other niche alternatives
    Mention of other keyboard layouts that are lesser know but also highlight some cool things about their design and practicallity
- Alternate physical keyboards
  - All of the options
  - Research on generic keyboards
    Talk about the 100%, 60%, 45% and what each one does well or doesn't do well
  - Optimized and esoteric keyboards
    - Split keyboards
    - Ortholinear keyboards
    - Curved keyboards
    - Glove type keyboards
  - Layers
    - General layer
    - Symbol layer
    - Function layer
    - Misc layer
- Personal keyboard and layout
- AI enhanced keyboards
  - Previous research
  - Personal experiment
    - Building the AI model
    - Testing the model
    - Refining the model
    - Data analysis & Conclusions
    - Future parameters to add

## Other things to talk about

- Typing Speed
  - So many things to say that I won't worry about this now
- Touchscreen keyboard layouts
  - What makes a good touch screen keyboard (only two fingers)
- Best two finger keyboard layout
- Alternative languages

---

## Genetic & Evolutionary Algorithms

### Date: XXXXXX

**Objective**: Research and gain a better understanding of modern literature on genetic algorithms for the purpose of optimizing a keyboard layout using machine learning.

Machine learning is a good way to get an optimized result using statistics and math. Genetic and evolutionary algorithms are a subset of this that simulation an environment with natural selection where only the best get to reproduce. In the case of this research, only the best keyboard that is tested to be the best gets to reproduce and mutate into a better keyboard.

Implementing this involves two approaches:

1. Mutations: Mutating a keyboard is easy. Take the best keyboard and then make random switches between the keys a certain number of times and then test the new keyboard to see if it is better. This is simple but it doesn't work really well. It relies heavily on luck to get to the best keyboard and follows more of a logarithmic progression on advancement.
2. Crossover: This approach is about taking the best keyboard layouts and then merging them to make a (hopefully) better keyboard. This is probably the best approach but it not easy to implement. There will have to be more research on this topic in the future before an actual implementation can take place.

---

## Setting Up Environment

### Date: XXXXXX

**Objective**: Map out and start work on creating an evironment for development on the code that generates the optimized keyboard layouts based on a genetic algorithm.

For this project, C++ is going to be the prefered language because of how fast it is. This language is known as the benchmark to test how slow other languages are so in this case, it will handle the large amonut of data processing that will take place. The specefic programming environment is Neovim, a highly customizable text editor that is lightweight but powerful.

The folder structure will resemble something like this:

```
.
├── README.md
├── research.md
├── research.pdf
└── src
   ├── Makefile
   ├── main.cpp
   ├── analysis.cpp
   ├── utils.cpp
   └── data
      ├── quotes.json
      ├── cpp.json
      └── python.json
```

**Features**:

- Here, there is a folder that will contain all of the source code `src`.
- In here, there is a `Makefile` that will be able to actually build the application. Essentially, a `Makefile` is a file that runs a bunch of `bash` programming to build the executable file that will run the genetic algorithm.
- The `main.cpp`, `analysis.cpp`, and `utils.cpp` files are all source code files with their own uses.
- The `data` directory holds the training data that is used to actually train these keyboard layouts. Each different set of data will result is different keyboard layouts. For example, a layout optimized for normal English will be different than a layout optimized for C++ programming.

---

## Parameterizing Training Data

### Date: XXXXXX

**Objective**: Formulate a way to quantify how good a keyboard layout is.

**Features To Track**:

1. The most important factor to a good keyboard is the finger distance traveled. A keyboard that makes you move your fingers all around the keyboard when typing is objectively worse than one that allows you to type mostly on the home row.
2. The amonut of effort it takes to hit the key. The index fingers and middle fingers are both much stronger than the pinky fingers. Therefore, more important letters sholud tend to hover around stronger fingers. There are also middle keys that are really incovienint and two middle keys that are a pain to reach.
3. Bigrams and trigrams are also important. Not so much as the speed of typing but the overall typing experience. It feels much better to type inwards from the pink to the ring to the middle to the index finger and akward when typing outwardly. Common bigrams such as "th" and "ch" and trigrams such as "the" and "cha" should typically follow this pattern of inward typing.

Taking these aspects into account, an array can be constructed that represents the importance and effort for each key on the keyboard.

**C++ Implementation**:

```cpp
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
```

In this senario, the keyboard has a total of 30 keys, 10 keys for each row. These are good approximate values for the distances the finger needs to travel and the effort that it would take to type that key.

**Example Layout**:

```cpp
std::vector<char> qwertyLayout = {
	'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
	'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
	'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?'
};
```

---

## Quantifying A Keyboard

### Date: XXXXXX

**Objective**: Construct an equation that will be used to test how good a keyboard is by using the parameterization techniques.

In order to start the machine learning process, there needs to be a good way to test how good a keyboard is. The simplest way to do this is to take a letter from the dataset and find the finger distance needed to press it and then go to the next letter and on and on. This way, after going through all of the training data, all of the letters have been testing and the total distance traveled is tracked.

---

## Finding Datasets

### Date: XXXXXX

**Objective**: Find a good dataset that can be used to train the machine learning algorithm.

The dataset for this project is going to be a dataset from huggingface, a online platform that has resources for training AI models. Credit goes to Abirate for making the dataset and sharing it publicly with free use. The dataset is composed of thousands of english quotes that is perfect for this machine learning project.

[Abirate/english_quotes](https://huggingface.co/datasets/Abirate/english_quotes)

In the C++ code, a simple integration of finding an english quote would look something like this:

```cpp
// Find a random quote in the JSONL file
string getRandomQuote() {
	string filename = "data/quotes.jsonl";
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
```

Here, we grab a random quote from our dataset, clean it up with regex and then return it. This function can be used to create a large and random body of text that semi-accurately represents the english language. In the future, this function could be improved if it took in any text file. This would make it easier to train based on small little dataset and find the perfect keyboard for that task. For example, a text file with someone's english paper could train the AI to make the best keyboard layout for typing that particiular essay.

---

## Building A Minimum Working Product

### Date: XXXXXX

**Objective**: Create a minimum working product for the algorithm and make it slowly optimize generations of keyboard layouts.

For this minimum working product, the features will be limited for the goal of making sure that they work in practice.

**Features**:

- Generations: each generation of keyboards are made up of the best keyboard layout in the past but mutated randomly.
- Mutations: Keyboard layouts in each generations have mutations in the hope that they randomly become a better keyboard layout.
- Data: A random set of english quotes are stringed together to make the training data for that keyboard.
- Logging: A short summary of the results are output every couple of generations to track the optimization progression.

**Constants**:

Some helpful constants for the generational runs. These can be optimized too but through trail and error.

```cpp
const int KEY_COUNT = 30;
const int NUM_KEYBOARDS = 12;
const int MAX_MUTATIONS = 100;
const int NUM_GENERATIONS = 1000;
const int NUM_GEN_QUOTES = 100;
```

**Genetic Algorithm Code**:

```cpp
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
```

Keyboard layouts evolve through mutations. These mutations are simple and are a basic swap of two random keys on the keyboard a certain number of times.

**Mutation Code**:

```cpp
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
```
