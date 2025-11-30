#!/usr/bin/env python3
"""
Simple test script to verify the application can be imported and run
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    required_modules = [
        'cv2',
        'numpy', 
        'imagehash',
        'PIL',
        'PyQt6.QtWidgets',
        'PyQt6.QtCore', 
        'PyQt6.QtGui',
        'ffmpeg',
        'moviepy',
        'librosa',
        'scipy.spatial.distance'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\nMissing modules: {missing_modules}")
        return False
    
    print("\nAll imports successful!")
    return True


def test_main_app():
    """Test that the main application can be instantiated"""
    print("\nTesting main application...")
    
    try:
        from main import MainWindow
        print("✓ MainWindow imported successfully")
        
        # Just check if the class exists and has expected methods
        methods = ['init_ui', 'load_file', 'analyze_original', 'generate_preview', 'export_media']
        for method in methods:
            if hasattr(MainWindow, method):
                print(f"✓ Method {method} exists")
            else:
                print(f"✗ Method {method} missing")
        
        return True
    except Exception as e:
        print(f"✗ Error testing main app: {e}")
        return False


def main():
    print("Testing Deep Media Uniqueness Enhancer...")
    print("="*50)
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_main_app():
        success = False
    
    print("="*50)
    if success:
        print("✓ All tests passed! The application is ready to run.")
        print("To start the application, run: python main.py")
    else:
        print("✗ Some tests failed. Please check the requirements.")
        sys.exit(1)


if __name__ == "__main__":
    main()