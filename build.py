#!/usr/bin/env python3
"""
Nuitka build script for Media Uniqueness Enhancer
Creates a single executable file for Windows distribution
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
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing Nuitka: {e}")
        return False


def build_single_executable():
    """Build a single executable file using Nuitka"""
    print("Building single executable with Nuitka...")
    
    # Prepare build command
    build_cmd = [
        sys.executable,
        "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--windows-disable-console",  # For GUI version
        "--windows-company-name=Media Enhancer",
        "--windows-product-name=Media Uniqueness Enhancer",
        "--windows-file-version=1.0.0",
        "--windows-product-version=1.0.0",
        "--include-data-file=README.md=README.md",
        "--include-data-file=requirements.txt=requirements.txt",
        # Include packages that are used in the application
        "--include-package=PyQt6",
        "--include-package=PyQt6.QtCore",
        "--include-package=PyQt6.QtGui", 
        "--include-package=PyQt6.QtWidgets",
        "--include-package=cv2",
        "--include-package=imagehash",
        "--include-package=numpy",
        "--include-package=PIL",
        "--include-package=moviepy",
        "--include-package=librosa",
        "--include-package=librosa.core",
        "--include-package=librosa.feature",
        "--include-package=librosa.util",
        "--include-package=librosa.effects",
        "--include-package=ffmpeg",
        "--include-package=ffmpeg_python",
        "--include-package=scipy",
        "--include-package=scipy.spatial",
        "--include-package=scipy.linalg",
        "--include-package=tqdm",
        "--remove-output",
        "--output-filename=MediaUniquenessEnhancer.exe",
        "main.py"
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("GUI executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during GUI build: {e}")
        return False


def build_cli_executable():
    """Build a CLI version of the executable"""
    print("Building CLI executable with Nuitka...")
    
    # Prepare build command without --windows-disable-console
    build_cmd = [
        sys.executable,
        "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--windows-company-name=Media Enhancer",
        "--windows-product-name=Media Uniqueness Enhancer CLI",
        "--windows-file-version=1.0.0",
        "--windows-product-version=1.0.0",
        "--include-data-file=README.md=README.md",
        "--include-data-file=requirements.txt=requirements.txt",
        # Include packages that are used in the application
        "--include-package=PyQt6",
        "--include-package=PyQt6.QtCore",
        "--include-package=PyQt6.QtGui", 
        "--include-package=PyQt6.QtWidgets",
        "--include-package=cv2",
        "--include-package=imagehash",
        "--include-package=numpy",
        "--include-package=PIL",
        "--include-package=moviepy",
        "--include-package=librosa",
        "--include-package=librosa.core",
        "--include-package=librosa.feature",
        "--include-package=librosa.util",
        "--include-package=librosa.effects",
        "--include-package=ffmpeg",
        "--include-package=ffmpeg_python",
        "--include-package=scipy",
        "--include-package=scipy.spatial",
        "--include-package=scipy.linalg",
        "--include-package=tqdm",
        "--remove-output",
        "--output-filename=MediaUniquenessEnhancer_CLI.exe",
        "main.py"
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("CLI executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during CLI build: {e}")
        return False


def main():
    print("Nuitka Builder for Media Uniqueness Enhancer")
    print("="*50)
    
    # Create dist directory
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    # Install Nuitka
    if not install_nuitka():
        print("Failed to install Nuitka. Exiting.")
        sys.exit(1)
    
    # Build executables
    gui_success = build_single_executable()
    
    if gui_success:
        # Move the executable to dist folder
        if Path("MediaUniquenessEnhancer.exe").exists():
            shutil.move("MediaUniquenessEnhancer.exe", dist_dir / "MediaUniquenessEnhancer.exe")
            print(f"GUI executable moved to {dist_dir / 'MediaUniquenessEnhancer.exe'}")
    
    cli_success = build_cli_executable()
    
    if cli_success:
        # Move the CLI executable to dist folder
        if Path("MediaUniquenessEnhancer_CLI.exe").exists():
            shutil.move("MediaUniquenessEnhancer_CLI.exe", dist_dir / "MediaUniquenessEnhancer_CLI.exe")
            print(f"CLI executable moved to {dist_dir / 'MediaUniquenessEnhancer_CLI.exe'}")
    
    print("\n" + "="*50)
    if gui_success and cli_success:
        print("Build completed successfully!")
        print(f"Files created in {dist_dir}:")
        print(f"  - MediaUniquenessEnhancer.exe (GUI version)")
        print(f"  - MediaUniquenessEnhancer_CLI.exe (CLI version)")
        print("\nUsage:")
        print("  GUI: Double-click MediaUniquenessEnhancer.exe")
        print("  CLI: MediaUniquenessEnhancer_CLI.exe --cli input.mp4 output.mp4 3")
    else:
        print("Build failed!")
        if not gui_success:
            print("  - GUI build failed")
        if not cli_success:
            print("  - CLI build failed")
        sys.exit(1)


if __name__ == "__main__":
    main()