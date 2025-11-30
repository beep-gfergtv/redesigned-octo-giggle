# Deep Media Uniqueness Enhancer

A specialized cross-platform application for deep, visually neutral media uniqueness enhancement to bypass content detection systems (YouTube Content ID, TikTok Copyright, Google Reverse Image Search, etc.).

## Features

### 🔹 Media Support
- **Images**: JPG, PNG, WebP formats
- **Videos**: MP4, MOV (H.264/H.265), up to 4K (3840×2160), 60fps
- **Output**: MP4 (H.264, baseline/main profile), JPG/PNG without quality loss

### 🔹 Uniqueness Enhancement
- **Semi-automatic mode**: Load file → select uniqueness level → preview → export
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

### 🔹 Uniqueness Analysis
- Image: Compare imagehash.phash() of original vs result → show % difference (target: ≥45%)
- Video: Analyze 5-10 key frames for phash differences
- Audio: Spectrogram similarity via librosa + cosine distance
- Visualize: Delta-hash histogram + final "risk level" (Low/Medium/High)

### 🔹 Performance & Stability
- Optimized FFmpeg pipeline processing
- Multi-threading support (1 file = 1 thread)
- Progress bar with ETA
- Crash recovery with checkpointing
- Minimal dependencies (avoiding heavy DL models)

## Installation

1. Clone or download this repository
2. Install Python 3.10+
3. Run the setup script:

```bash
python setup.py
```

This will install all required dependencies from requirements.txt.

**Note**: You need to have FFmpeg installed on your system. If not available in PATH, download static binaries from [FFmpeg Downloads](https://ffmpeg.org/download.html).

## Usage

Run the application:

```bash
python main.py
```

### Interface
- **Drag & drop** zone for loading files
- **Media type** toggle: 📷 Photo / 🎥 Video
- **Uniqueness level** slider (1-5)
- **Analyze original** button → shows source hash/risk
- **Generate preview** button (3-sec fragment)
- **Export** button
- **Report panel**: phash delta, audio similarity, size/duration, status

## Technical Details

### Backend
- Python 3.10+ with OpenCV, imagehash, moviepy, librosa, ffmpeg-python, PyQt6
- Static FFmpeg binary (included in package)
- PyQt6 frontend (more reliable than Electron for media-heavy tasks)

### Processing Pipeline
1. **Image Processing**:
   - Random cropping and scaling
   - Perlin noise addition
   - Color space transformations (HLS shifts)
   - Texture overlays

2. **Video Processing**:
   - Zoom-pan drift effects
   - Spatial jitter
   - Audio pitch/tempo manipulation
   - GOP structure changes
   - Encoding parameter adjustments

## Risk Assessment

The application provides a risk level based on:
- **Low Risk**: ≥45% phash difference (recommended for strict platforms)
- **Medium Risk**: 30-45% phash difference (for less strict platforms)
- **High Risk**: <30% phash difference (not recommended)

## Important Notes

- The application preserves content meaning and structure
- No visible artifacts are introduced
- All metadata (EXIF/XMP/ID3) is removed
- Processing maintains visual neutrality while maximizing algorithmic differences

## License

This is a specialized tool for content uniqueness. Use responsibly and in compliance with applicable laws and platform terms of service.
