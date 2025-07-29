#!/bin/bash

# Navigate to the project directory
cd /home/sam/birthday-alert

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Run the Python script
python birthday-alert.py

# Deactivate the virtual environment
deactivate