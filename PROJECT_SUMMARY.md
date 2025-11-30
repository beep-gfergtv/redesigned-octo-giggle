# Deep Media Uniqueness Enhancer - Project Summary

## Overview
A specialized cross-platform application for deep, visually neutral media uniqueness enhancement to bypass content detection systems (YouTube Content ID, TikTok Copyright, Google Reverse Image Search, etc.).

## Files Created

### Core Application
- `main.py` - Main PyQt6 application with GUI interface and all processing logic
- `requirements.txt` - Python dependencies list
- `setup.py` - Installation script

### Documentation
- `README.md` - Comprehensive user guide
- `PROJECT_SUMMARY.md` - This file

### Test/Demo
- `test_app.py` - Verification script for dependencies and functionality
- `demo.py` - Demonstration of application capabilities
- `demo_original.jpg` - Sample original image for testing
- `demo_processed.jpg` - Sample processed image for testing

## Key Features Implemented

### 🔹 Media Support
- **Images**: JPG, PNG, WebP formats
- **Videos**: MP4, MOV (H.264/H.265), up to 4K (3840×2160), 60fps
- **Output**: MP4 (H.264, baseline/main profile), JPG/PNG without quality loss

### 🔹 Uniqueness Enhancement
- **For Images (perceptual hash disruption)**:
  - Random cropping (2-6%) + scaling (±3%)
  - Light perspective warp (max 0.8%)
  - Animated or static Perlin noise (0.4% opacity)
  - Frame-level micro color shifts (H±1°, S±2%, L±3%)
  - Optional high-frequency texture overlay
- **For Videos (fingerprint evasion)**:
  - Smooth zoom-pan drift (0.5% per second)
  - Frame-level spatial jitter (1-2 px, pseudo-random)
  - Dynamic vignette (center following frame CoM)
  - Recoding with modified GOP (keyint=30±5), B-frames=3
  - Audio pitch shift +2.3% with tempo compensation
  - Low-cut and high-shelf filters
  - Ultrasound noise and reverb

### 🔹 Analysis & Reporting
- Image: Compare imagehash.phash() of original vs result → show % difference
- Video: Analyze 5-10 key frames for phash differences
- Audio: Spectrogram similarity via librosa + cosine distance
- Risk assessment: "Low" (≥45%), "Medium" (30-45%), "High" (<30%)

### 🔹 User Interface
- Drag & drop zone for loading files
- Media type toggle: 📷 Photo / 🎥 Video
- Uniqueness level slider (1-5)
- "Analyze original" button → shows source hash/risk
- "Generate preview" button (3-sec fragment)
- "Export" button
- Report panel: phash delta, audio similarity, size/duration, status

## Technical Stack
- **Backend**: Python 3.10+ with OpenCV, imagehash, moviepy, librosa, ffmpeg-python, PyQt6
- **Frontend**: PyQt6 for reliable cross-platform GUI
- **Processing**: Optimized FFmpeg pipeline
- **Platform**: Cross-platform (Windows, macOS, Linux)

## Installation & Usage

### Installation:
```bash
python setup.py
```

### Usage:
```bash
python main.py
```

## Risk Assessment
The application provides risk levels based on perceptual hash differences:
- **Low Risk**: ≥45% phash difference (recommended for strict platforms)
- **Medium Risk**: 30-45% phash difference (for less strict platforms)
- **High Risk**: <30% phash difference (not recommended)

## Compliance Notes
- Preserves content meaning and structure
- No visible artifacts introduced
- All metadata (EXIF/XMP/ID3) is removed
- Processing maintains visual neutrality while maximizing algorithmic differences
- Use responsibly and in compliance with applicable laws and platform terms of service