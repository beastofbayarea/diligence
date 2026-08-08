"""
dashboard.py — Main entry point alias for Streamlit Cloud deployment.
Forwards execution to app.py.
"""
import runpy
import os
import sys

# Ensure current working directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Execute app.py in the main module scope
runpy.run_path(os.path.join(os.path.dirname(__file__), "app.py"), run_name="__main__")
