# Deep Media Uniqueness Enhancer

A semi-automatic application for enhancing media uniqueness to bypass content detection systems like YouTube Content ID and TikTok copyright detectors.

## Features

- ✅ Semi-automatic mode: User selects level → preview → export
- ✅ Built-in uniqueness analysis (before/after)
- ✅ Minimal GUI (PyQt6) + console mode (optional via --cli)
- ✅ Single executable output via Nuitka compilation
- ✅ Supports both images and videos

## Requirements

- Python 3.9-3.11
- FFmpeg (for video processing)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install FFmpeg (for video processing):
   - Download from: https://ffmpeg.org/download.html
   - Add to system PATH

## Usage

### GUI Mode
```bash
python main.py
```

### CLI Mode
```bash
python main.py --cli <input_file> <output_file> <level>
# Level: 1 (Low), 2 (Medium), 3 (High)
```

## Building with Nuitka

To compile to a single executable (Windows):

**Note**: The following commands should be run on a Windows machine with Python and Nuitka installed.

```bash
pip install nuitka
python -m nuitka --standalone --onefile --windows-disable-console --include-package=PyQt6 --include-package=cv2 --include-package=imagehash --include-package=numpy --include-package=PIL --include-package=moviepy --include-package=librosa --include-package=ffmpeg --include-package=scipy --include-package=tqdm main.py
```

For CLI version (with console):
```bash
python -m nuitka --standalone --onefile --include-package=PyQt6 --include-package=cv2 --include-package=imagehash --include-package=numpy --include-package=PIL --include-package=moviepy --include-package=librosa --include-package=ffmpeg --include-package=scipy --include-package=tqdm main.py
```

## How It Works

### For Images:
- Random cropping (2-6% depending on level)
- Slight scaling (0.97-1.03x depending on level)
- Perlin noise addition
- HLS color space shifts
- Perceptual hash analysis for uniqueness measurement

### For Videos:
- Zoom/pan drift over time
- Spatial noise addition
- Audio pitch/tempo modification
- GOP size and CRF adjustments
- Keyframe-based uniqueness analysis

## Risk Assessment

The application provides risk level assessment:
- **Low Risk**: >45% perceptual hash difference
- **Medium Risk**: 30-45% perceptual hash difference  
- **High Risk**: <30% perceptual hash difference

## Technical Details

The application uses:
- PyQt6 for the GUI
- OpenCV for image/video processing
- FFmpeg-python for video encoding
- ImageHash for perceptual analysis
- MoviePy for video manipulation
- Librosa for audio analysis
- NumPy/SciPy for mathematical operations
