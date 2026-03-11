#!/usr/bin/env python
"""
Quick Start Script - Nexus AI Backend
Run this script to validate and start the server
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Verify Python 3.8+ is installed."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True


def check_venv():
    """Check if virtual environment is activated."""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if not in_venv:
        print("⚠️  Virtual environment not detected")
        print("     Activate with: source .venv/bin/activate (macOS/Linux)")
        print("                 or .venv\\Scripts\\activate (Windows)")
        return False
    print("✅ Virtual environment detected")
    return True


def check_env_file():
    """Check if .env file exists."""
    if not Path(".env").exists():
        print("⚠️  .env file not found")
        print("     Creating from template...")
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ .env file created from .env.example")
            print("   Please edit .env with your actual credentials")
            return False
        else:
            print("❌ .env.example not found either")
            return False
    print("✅ .env file found")
    return True


def check_dependencies():
    """Verify required packages are installed."""
    try:
        import fastapi
        import firebase_admin
        import google.generativeai as genai
        from pydantic import BaseModel
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        return False


def check_firebase_credentials():
    """Check Firebase credentials file."""
    if Path("serviceAccountKey.json").exists():
        print("✅ Firebase credentials found (serviceAccountKey.json)")
        return True
    
    print("⚠️  Firebase credentials file not found")
    print("   Please add serviceAccountKey.json to project root")
    return False


def check_api_key():
    """Verify GEMINI_API_KEY is set."""
    if os.getenv("GEMINI_API_KEY"):
        print("✅ GEMINI_API_KEY is set")
        return True
    else:
        print("❌ GEMINI_API_KEY environment variable not set")
        print("   Add to .env file or set in terminal:")
        print("   export GEMINI_API_KEY=your_key_here")
        return False


def main():
    """Run all checks and start server if everything is valid."""
    print("\n" + "="*50)
    print("🚀 Nexus AI Backend - Quick Start")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_venv),
        (".env File", check_env_file),
        ("Dependencies", check_dependencies),
        ("Firebase Credentials", check_firebase_credentials),
        ("API Key", check_api_key),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*50)
    if all(results):
        print("✅ All checks passed!")
        print("="*50 + "\n")
        
        print("🚀 Starting Nexus AI Backend Server...")
        print("📡 Server will be available at: http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop the server\n")
        
        try:
            subprocess.run([sys.executable, "run.py"], check=True)
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped gracefully")
    else:
        print("❌ Some checks failed")
        print("   Please fix the issues above and try again")
        print("="*50)
        sys.exit(1)


if __name__ == "__main__":
    main()
