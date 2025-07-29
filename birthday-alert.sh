#!/bin/bash

# Navigate to the project directory
cd /home/sam/birthday-alert


# Check if the virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirments.txt

# Run the Python script
python birthday-alert.py

# Deactivate the virtual environment
deactivate