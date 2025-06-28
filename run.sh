#!/bin/bash
"""
Launcher script for Mentorship System
This script starts the Flask application with proper virtual environment setup
"""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "🎓 MENTORSHIP MANAGEMENT SYSTEM"
echo "============================================================"

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created successfully!"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
if [ -f "requirements.txt" ]; then
    echo "🔧 Installing/updating requirements..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install requirements"
        exit 1
    fi
    echo "✅ Requirements installed successfully!"
fi

echo "🔧 Initializing database..."
echo "🌐 Starting web server..."

# Get port from environment or use 5000
PORT=${PORT:-5000}
HOST=${HOST:-0.0.0.0}

echo "✅ Server starting on $HOST:$PORT"
echo "🛑 Press Ctrl+C to stop the server"

# Check if running in Codespace
if [ ! -z "$CODESPACE_NAME" ]; then
    CODESPACE_URL="https://${CODESPACE_NAME}-${PORT}.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-preview.app.github.dev}"
    echo "🌍 Codespace URL: $CODESPACE_URL"
else
    LOCAL_URL="http://localhost:$PORT"
    echo "🏠 Local URL: $LOCAL_URL"
fi

echo "============================================================"

# Run the Flask application
python app.py
