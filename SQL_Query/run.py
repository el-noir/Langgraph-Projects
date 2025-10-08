#!/usr/bin/env python3
"""
Startup script for SQL Query Assistant
"""

import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import streamlit
        import langgraph
        import langchain_google_genai
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("Please copy .env.example to .env and add your Google API key")
        return False
    print("✅ .env file found")
    return True

def main():
    """Main startup function"""
    print("🚀 Starting SQL Query Assistant...")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment file
    if not check_env_file():
        print("You can still run the app, but you'll need to set GOOGLE_API_KEY")
    
    # Start Streamlit
    print("🌐 Launching Streamlit application...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
