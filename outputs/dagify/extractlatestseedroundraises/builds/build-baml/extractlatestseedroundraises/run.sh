#!/bin/bash
set -e

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set."
    echo "Please set it before running this script with:"
    echo "export OPENAI_API_KEY='your-api-key'"
    echo "This key is required for the BAML workflow to make API calls to OpenAI."
    exit 1
fi

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    # Make sure this is Python 3
    PYTHON_VERSION=$(python -c 'import sys; print(sys.version_info.major)')
    if [[ "$PYTHON_VERSION" == "3" ]]; then
        PYTHON=python
    else
        echo "Python 3 is required but found Python $PYTHON_VERSION."
        exit 1
    fi
else
    echo "Python 3 is required but not found. Please install Python 3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate || source .venv/Scripts/activate

# Set environment variables
export BAML_LOG=OFF

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Always regenerate BAML client code to ensure it matches the latest BAML definitions
echo "Generating BAML client code..."
baml-cli generate

# Run the workflow
echo "Running workflow..."
python main.py
