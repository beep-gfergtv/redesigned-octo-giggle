#!/usr/bin/env python3
"""
Build script for compiling the Media Uniqueness Enhancer with Nuitka
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def install_nuitka():
    """Install Nuitka if not already installed"""
    print("Installing Nuitka...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nuitka"])
        print("Nuitka installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Nuitka: {e}")
        return False
    return True


def build_executable():
    """Build the executable with Nuitka"""
    print("Building executable with Nuitka...")
    
    # Nuitka build command with optimizations for minimal size
    build_cmd = [
        sys.executable,
        "-m", "nuitka",
        "--standalone",
        "--onefile",  # Single executable
        "--windows-disable-console",  # Remove console window for GUI
        "--include-data-files=.",  # Include necessary data files
        "--include-package=PyQt6",
        "--include-package=cv2",
        "--include-package=imagehash",
        "--include-package=numpy",
        "--include-package=PIL",
        "--include-package=moviepy",
        "--include-package=librosa",
        "--include-package=ffmpeg",
        "--include-package=scipy",
        "--include-package=tqdm",
        "--remove-output",
        "--output-filename=MediaUniquenessEnhancer.exe",
        "--output-dir=dist",
        "main.py"
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        return False


def build_executable_with_cli():
    """Build the executable with console support for CLI mode"""
    print("Building executable with CLI support...")
    
    # Nuitka build command with console for CLI mode
    build_cmd = [
        sys.executable,
        "-m", "nuitka",
        "--standalone",
        "--onefile",  # Single executable
        "--include-package=PyQt6",
        "--include-package=cv2",
        "--include-package=imagehash",
        "--include-package=numpy",
        "--include-package=PIL",
        "--include-package=moviepy",
        "--include-package=librosa",
        "--include-package=ffmpeg",
        "--include-package=scipy",
        "--include-package=tqdm",
        "--remove-output",
        "--output-filename=MediaUniquenessEnhancer_CLI.exe",
        "--output-dir=dist",
        "main.py"
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("CLI build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during CLI build: {e}")
        return False


def main():
    print("Building Media Uniqueness Enhancer with Nuitka...")
    
    # Create dist directory
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    # Install Nuitka
    if not install_nuitka():
        print("Failed to install Nuitka. Exiting.")
        sys.exit(1)
    
    # Build GUI version (without console)
    success_gui = build_executable()
    
    # Build CLI version (with console)
    success_cli = build_executable_with_cli()
    
    if success_gui and success_cli:
        print("\nBuild completed successfully!")
        print(f"GUI executable: {dist_dir}/MediaUniquenessEnhancer.exe")
        print(f"CLI executable: {dist_dir}/MediaUniquenessEnhancer_CLI.exe")
        print("\nTo run in GUI mode: double-click the .exe file")
        print("To run in CLI mode: python MediaUniquenessEnhancer_CLI.exe --cli")
    else:
        print("\nBuild failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()