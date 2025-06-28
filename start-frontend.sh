#!/bin/bash

# Start Frontend Server
echo "Starting Frontend Server..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Start React app
echo "Starting React application on http://localhost:3000"
npm start
