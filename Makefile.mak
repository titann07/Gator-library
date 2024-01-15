# Makefile for Gator Library Management System

# Compiler and flags
PYTHON = python3
PYTEST = pytest
SRC_DIR = src
TEST_DIR = tests
OUTPUT_DIR = output

# Main source file
MAIN_FILE = main.py

# Test files
TEST_FILES = test_*.py

# Input and output file names
INPUT_FILE = inputs.txt
OUTPUT_FILE = output.txt

# Targets and their recipes
all: run

run:
	@$(PYTHON) $(SRC_DIR)/$(MAIN_FILE) $(INPUT_FILE)

test:
	@$(PYTEST) $(TEST_DIR)

clean:
	@rm -rf $(OUTPUT_DIR)

.PHONY: all run test clean
