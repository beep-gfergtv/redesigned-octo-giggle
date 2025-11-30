#!/usr/bin/env python3
"""
Setup script for Deep Media Uniqueness Enhancer
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def install_dependencies():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    return True


def download_ffmpeg():
    """Download static FFmpeg binaries if not present"""
    print("Checking for FFmpeg...")
    
    # Check if ffmpeg is available in PATH
    try:
        subprocess.check_call(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("FFmpeg is already available in system PATH")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg not found in system PATH, will need to install manually")
        print("Please install FFmpeg manually or download static binaries from:")
        print("https://ffmpeg.org/download.html")
        return False


def main():
    print("Setting up Deep Media Uniqueness Enhancer...")
    
    # Install Python dependencies
    if not install_dependencies():
        print("Failed to install dependencies. Exiting.")
        sys.exit(1)
    
    # Check for FFmpeg
    download_ffmpeg()
    
    print("\nSetup completed!")
    print("To run the application, execute: python main.py")


if __name__ == "__main__":
    main()