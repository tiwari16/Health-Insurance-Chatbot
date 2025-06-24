#!/bin/bash

echo "Deactivating any active virtual environment..."
deactivate 2>/dev/null

echo "Removing old virtual environment..."
rm -rf venv

echo "Creating new virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing Streamlit..."
python -m pip install streamlit

echo "Virtual environment reset complete!"
echo "Run 'source venv/bin/activate' to start using the environment."
echo "You can now run your Streamlit application."
echo "To deactivate the virtual environment, use 'deactivate'."
echo "To remove the virtual environment, run this script again."
echo "Happy coding!"