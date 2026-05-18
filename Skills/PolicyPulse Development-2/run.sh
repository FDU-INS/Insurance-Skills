#!/bin/bash

# PolicyPulse - Launcher Script
# Run this to start the PolicyPulse application

echo "🚀 Starting PolicyPulse..."
echo ""

# Check if conda environment exists
if ! conda env list | grep -q "^policy "; then
    echo "❌ Error: conda environment 'policy' not found"
    echo "Please create it first with: conda create -n policy python=3.10"
    exit 1
fi

# Activate environment and run
cd /home/uzwalpandey/Documents/PolicyPulse

echo "📂 Directory: $(pwd)"
echo "🐍 Activating conda environment 'policy'..."
echo ""

conda run -n policy streamlit run src/app.py

# If that fails, try alternative method
if [ $? -ne 0 ]; then
    echo ""
    echo "Trying alternative method..."
    conda activate policy && streamlit run src/app.py
fi
