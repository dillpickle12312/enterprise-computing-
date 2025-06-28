#!/bin/bash
# Quick setup script for the Mentorship System

echo "============================================================"
echo "🎓 MENTORSHIP SYSTEM - QUICK SETUP"
echo "============================================================"

# Change to script directory
cd "$(dirname "$0")"

echo "🔧 Setting up virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "🔧 Installing requirements..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  ./run.sh"
echo "or"
echo "  python run_online.py"
echo ""
echo "============================================================"
