#!/usr/bin/env python3
"""
Demo script showing the capabilities of the Deep Media Uniqueness Enhancer
This script creates a simple example of how the application works
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image
import imagehash
import tempfile
import shutil
from pathlib import Path

def create_demo_image():
    """Create a simple demo image for testing"""
    # Create a simple image with some pattern
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Add some colored rectangles
    cv2.rectangle(img, (50, 50), (200, 150), (255, 0, 0), -1)  # Blue
    cv2.rectangle(img, (300, 100), (500, 200), (0, 255, 0), -1)  # Green
    cv2.rectangle(img, (150, 250), (400, 350), (0, 0, 255), -1)  # Red
    
    # Add some text
    cv2.putText(img, 'DEMO', (220, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    return img

def demonstrate_image_processing():
    """Demonstrate image uniqueness processing"""
    print(" Demonstrating Image Processing ")
    print("=" * 50)
    
    # Create original image
    original_img = create_demo_image()
    original_path = "demo_original.jpg"
    cv2.imwrite(original_path, original_img)
    
    # Calculate original hash
    original_pil = Image.open(original_path)
    original_hash = imagehash.average_hash(original_pil)
    print(f"Original image hash: {original_hash}")
    
    # Apply simple transformations to simulate what the app does
    height, width = original_img.shape[:2]
    
    # Apply random crop (simulating 3% crop)
    crop_percent = 0.03
    crop_w = int(width * (1 - crop_percent))
    crop_h = int(height * (1 - crop_percent))
    start_x = int(crop_percent * width / 2)
    start_y = int(crop_percent * height / 2)
    cropped_img = original_img[start_y:start_y+crop_h, start_x:start_x+crop_w]
    
    # Resize back to original size
    processed_img = cv2.resize(cropped_img, (width, height))
    
    # Apply slight color shifts (simulating HLS shifts)
    hls = cv2.cvtColor(processed_img, cv2.COLOR_BGR2HLS)
    hls[:,:,0] = np.clip(hls[:,:,0] + 0.5, 0, 179)  # H channel
    hls[:,:,1] = np.clip(hls[:,:,1] + 1.5, 0, 255)  # L channel
    hls[:,:,2] = np.clip(hls[:,:,2] + 2.0, 0, 255)  # S channel
    processed_img = cv2.cvtColor(hls, cv2.COLOR_HLS2BGR)
    
    # Save processed image
    processed_path = "demo_processed.jpg"
    cv2.imwrite(processed_path, processed_img)
    
    # Calculate processed hash
    processed_pil = Image.open(processed_path)
    processed_hash = imagehash.average_hash(processed_pil)
    print(f"Processed image hash: {processed_hash}")
    
    # Calculate difference
    hash_diff = original_hash - processed_hash
    print(f"Hash difference: {hash_diff}")
    
    print(f"\nOriginal image saved as: {original_path}")
    print(f"Processed image saved as: {processed_path}")
    print("Both images are now available for comparison")
    print("=" * 50)

def show_application_features():
    """Show the features of the application"""
    print("\n Deep Media Uniqueness Enhancer Features ")
    print("=" * 50)
    
    features = [
        "🔹 Image formats: JPG, PNG, WebP",
        "🔹 Video formats: MP4, MOV (H.264/H.265), up to 4K",
        "🔹 Uniqueness levels: Low, Medium, High (1-5 scale)",
        "🔹 Visual preservation: No visible artifacts introduced",
        "🔹 Perceptual hash disruption for images",
        "🔹 Video fingerprint evasion techniques",
        "🔹 Audio processing with pitch/tempo compensation",
        "🔹 Real-time preview generation",
        "🔹 Risk assessment with phash delta calculation",
        "🔹 Cross-platform compatibility (Windows, macOS, Linux)",
        "🔹 Drag & drop interface",
        "🔹 FFmpeg optimized processing pipeline"
    ]
    
    for feature in features:
        print(feature)
    
    print("=" * 50)

def show_usage_instructions():
    """Show how to use the application"""
    print("\n How to Use the Application ")
    print("=" * 50)
    
    steps = [
        "1. Run the application: python main.py",
        "2. Select media type (Photo or Video)",
        "3. Drag & drop your file or click to select",
        "4. Choose uniqueness level (1-5)",
        "5. Click 'Analyze original' to see source hash",
        "6. Click 'Generate preview' to see sample output",
        "7. Click 'Export' to process and save the file",
        "8. Check the results panel for uniqueness metrics"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")
    
    print("=" * 50)

def main():
    print("Deep Media Uniqueness Enhancer - Demo")
    print("=====================================")
    
    # Show features
    show_application_features()
    
    # Demonstrate image processing
    demonstrate_image_processing()
    
    # Show usage instructions
    show_usage_instructions()
    
    print("\nTo run the full application:")
    print("python main.py")
    
    # Clean up demo files after a delay to let user see them
    print("\nDemo images created. You can view them before cleanup.")

if __name__ == "__main__":
    main()