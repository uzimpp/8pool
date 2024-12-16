#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up Pool Game...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 is not installed. Please install Python3 first.${NC}"
    exit 1
fi

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install --upgrade pip

# Check if pip is available, if not, try using Homebrew on macOS
if ! command -v pip &> /dev/null; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${RED}pip is not available. Trying to install packages using Homebrew...${NC}"
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}Homebrew is not installed. Please install Homebrew first.${NC}"
            exit 1
        fi
        brew install pylint python-tk
    else
        echo -e "${RED}pip is not available and the system is not macOS. Exiting...${NC}"
        exit 1
    fi
else
    pip install pylint python-tk
fi

# Check if system is Linux and install additional dependencies if needed
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing Linux dependencies..."
    sudo apt-get update
    sudo apt-get install -y python3-tk
fi

# Run pylint
echo "Running pylint..."
if pylint src/*.py; then
    echo -e "${GREEN}No issues found by pylint :D ${NC}\n"
else
    echo -e "${RED}Pylint has found some issues :(${NC}\n"
fi

# Run the game
echo -e "Starting the game..."
python3 src/poolsim.py

# Deactivate virtual environment
deactivate

echo -e "${GREEN}Done!${NC}" 