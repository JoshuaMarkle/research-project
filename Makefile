# Compiler settings
CC = g++
CFLAGS = -I./algorithm -I./struct -I./utils -I./data

# Define the directories for the build components
SRCDIR = src
OBJDIR = obj
BINDIR = bin

# Define your source files here
SOURCES := $(wildcard $(SRCDIR)/*.cpp) \
           $(wildcard $(SRCDIR)/algorithm/*.cpp) \
           $(wildcard $(SRCDIR)/struct/*.cpp) \
           $(wildcard $(SRCDIR)/utils/*.cpp)

# Define your object files here
OBJECTS := $(SOURCES:$(SRCDIR)/%.cpp=$(OBJDIR)/%.o)

# Define your executable file name here
EXECUTABLE := $(BINDIR)/main

all: $(BINDIR) $(OBJDIR) $(EXECUTABLE)
	@$(EXECUTABLE)

$(BINDIR):
	mkdir -p $@

$(OBJDIR):
	mkdir -p $@
	mkdir -p $@/algorithm
	mkdir -p $@/struct
	mkdir -p $@/utils

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $(OBJECTS)

$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(OBJDIR) $(EXECUTABLE)
