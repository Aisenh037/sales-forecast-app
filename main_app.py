"""
Enterprise SaaS Analytics Platform - Main Entry Point
Redirects to the main application
"""

# Import and run the main enterprise application
import subprocess
import sys

if __name__ == "__main__":
    # Run the enterprise SaaS platform
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"] + sys.argv[1:])