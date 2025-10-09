"""
Web Research Assistant API Startup Script
=========================================
"""

import sys
import subprocess
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'langchain',
        'langgraph',
        'langchain_google_genai',
        'langchain_tavily',
        'langchain_community'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_environment():
    """Check if environment variables are set"""
    required_env_vars = [
        'GOOGLE_API_KEY',
        'TAVILY_API_KEY'
    ]
    
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Set environment variables in your .env file or system environment")
        return False
    
    print("✅ All required environment variables are set")
    return True

def start_api():
    """Start the FastAPI application"""
    print("🚀 Starting Web Research Assistant API...")
    print("=" * 50)
    
    # Check prerequisites
    if not check_dependencies():
        return False
    
    if not check_environment():
        return False
    
    print("\n📊 LangGraph workflow integration enabled")
    print("🔍 Research endpoints will be available at http://localhost:8000")
    print("📖 API documentation at http://localhost:8000/docs")
    print("🧪 Test the API with: python test_api.py")
    print("\n⚡ Starting server...")
    print("-" * 50)
    
    try:
        # Start the API server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🌐 Web Research Assistant API Startup")
    print("=====================================")
    
    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success = start_api()
    
    if not success:
        print("\n❌ Failed to start API server")
        print("💡 Check the error messages above for details")
        sys.exit(1)