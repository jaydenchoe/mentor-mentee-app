#!/bin/bash

# Start Backend Server
echo "Starting Backend Server..."
cd backend

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Start Flask app
echo "Starting Flask application on http://localhost:8080"
python app.py
