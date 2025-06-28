#!/bin/bash

echo "Starting Frontend Development Server..."
cd "$(dirname "$0")"

# Start Python HTTP server
echo "Starting Python HTTP server on http://localhost:3000"
if command -v python3 &> /dev/null; then
    python3 -m http.server 3000
else
    python -m SimpleHTTPServer 3000
fi
