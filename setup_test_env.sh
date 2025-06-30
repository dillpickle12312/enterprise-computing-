#!/bin/bash
# Quick setup script for testing environment

echo "🚀 Setting up testing environment..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project root directory."
    exit 1
fi

# Try to install requirements if possible
echo "📦 Attempting to install requirements..."
if command -v python3 &> /dev/null; then
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
    elif python3 -m pip --version &> /dev/null; then
        python3 -m pip install -r requirements.txt
    else
        echo "⚠️  Warning: pip not available, some tests may fail"
    fi
else
    echo "❌ Error: Python3 not found"
    exit 1
fi

echo "✅ Setup complete!"
echo "🧪 Run the tests with: python3 manual_system_test.py"
