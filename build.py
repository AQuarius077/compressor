#!/usr/bin/env python3
"""
Build script for Universal File Compressor
Handles dependency installation and module building
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a shell command and handle errors"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    print("🚀 Building Universal File Compressor...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    
    # Install Python dependencies
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Build low-level module
    os.chdir("backend/lowlevel")
    if os.path.exists("lz77_core.asm"):
        print("\n🔨 Building assembly module...")
        if run_command("nasm -f elf64 lz77_core.asm -o lz77_core.o", "Assembling LZ77 core"):
            run_command(f"{sys.executable} setup.py build_ext --inplace", "Building C extension")
    os.chdir("../..")
    
    print("\n✨ Build completed successfully!")
    print("\nTo start the application:")
    print("1. Run the backend: python backend/app.py")
    print("2. Open frontend/index.html in your browser")
    print("\nOr use the quick start script: python start.py")

if __name__ == "__main__":
    main()