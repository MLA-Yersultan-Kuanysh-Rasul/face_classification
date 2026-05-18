#!/bin/bash

echo "========================================"
echo "Starting Face Detector..."
echo "========================================"
echo ""

if [ ! -f "venv/bin/activate" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run setup.sh first."
    exit 1
fi

if [ ! -f "model/best_model.h5" ]; then
    echo "Error: Model file not found!"
    echo "Please ensure model/best_model.h5 exists."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting Flask server..."
echo ""
echo "========================================"
echo "Application running at:"
echo "http://localhost:5000"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python app.py
