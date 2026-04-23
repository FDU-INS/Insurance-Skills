"""
PolicyPulse - Streamlit Cloud Entry Point

This file serves as the entry point for Streamlit Cloud deployment.
It sets up the Python path and then runs the main application.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import and run the main application
from src.app import main

# Call main() directly for Streamlit Cloud
main()
