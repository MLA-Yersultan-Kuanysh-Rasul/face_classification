#!/bin/bash

echo "========================================"
echo "Real vs Fake Face Detector - Setup"
echo "========================================"
echo ""

echo "[1/3] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "[2/3] Activating virtual environment..."
source venv/bin/activate

echo "[3/3] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Run: ./run.sh"
echo "  2. Open: http://localhost:5000"
echo ""
