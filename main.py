#!/usr/bin/env python3
"""
Deep Media Uniqueness Enhancer - Cross-platform Application
For bypassing content detection systems (YouTube Content ID, TikTok Copyright, etc.)
"""

import sys
import os
import cv2
import numpy as np
import imagehash
from PIL import Image
import tempfile
import hashlib
import json
from pathlib import Path
import ffmpeg
import random
import time
from moviepy import VideoFileClip, AudioFileClip
import librosa
from scipy.spatial.distance import cosine

# Import PyQt6 modules only when needed (for GUI mode)
def get_qt_modules():
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QPushButton, QLabel, QSlider, 
                                QFileDialog, QProgressBar, QTextEdit, QComboBox,
                                QGroupBox, QRadioButton, QButtonGroup)
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent
    return {
        'QApplication': QApplication,
        'QMainWindow': QMainWindow,
        'QWidget': QWidget,
        'QVBoxLayout': QVBoxLayout,
        'QHBoxLayout': QHBoxLayout,
        'QPushButton': QPushButton,
        'QLabel': QLabel,
        'QSlider': QSlider,
        'QFileDialog': QFileDialog,
        'QProgressBar': QProgressBar,
        'QTextEdit': QTextEdit,
        'QComboBox': QComboBox,
        'QGroupBox': QGroupBox,
        'QRadioButton': QRadioButton,
        'QButtonGroup': QButtonGroup,
        'Qt': Qt,
        'QThread': QThread,
        'pyqtSignal': pyqtSignal,
        'QTimer': QTimer,
        'QPixmap': QPixmap,
        'QDragEnterEvent': QDragEnterEvent,
        'QDropEvent': QDropEvent
    }


class MediaProcessor:
    """Handles all media processing operations"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def calculate_phash_difference(self, img1_path, img2_path):
        """Calculate perceptual hash difference between two images"""
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        
        hash1 = imagehash.phash(img1)
        hash2 = imagehash.phash(img2)
        
        # Calculate Hamming distance
        diff = hash1 - hash2
        max_diff = len(hash1.hash) * hash1.hash.dtype.itemsize * 8  # Max possible bits
        percentage = (diff / max_diff) * 100
        
        return percentage
    
    def process_image(self, input_path, output_path, level):
        """Apply uniqueness enhancement to an image based on level"""
        img = cv2.imread(input_path)
        height, width = img.shape[:2]
        
        # Level-based parameters
        if level == 1:  # Low
            crop_percent = random.uniform(0.02, 0.03)
            scale_factor = random.uniform(0.995, 1.005)
            noise_opacity = 0.002
            color_shift_h = random.uniform(-0.5, 0.5)
            color_shift_s = random.uniform(-1, 1)
            color_shift_l = random.uniform(-1.5, 1.5)
        elif level == 2:  # Medium
            crop_percent = random.uniform(0.02, 0.04)
            scale_factor = random.uniform(0.985, 1.015)
            noise_opacity = 0.003
            color_shift_h = random.uniform(-0.8, 0.8)
            color_shift_s = random.uniform(-1.5, 1.5)
            color_shift_l = random.uniform(-2.5, 2.5)
        else:  # High
            crop_percent = random.uniform(0.03, 0.06)
            scale_factor = random.uniform(0.97, 1.03)
            noise_opacity = 0.004
            color_shift_h = random.uniform(-1.0, 1.0)
            color_shift_s = random.uniform(-2.0, 2.0)
            color_shift_l = random.uniform(-3.0, 3.0)
        
        # Random crop
        crop_w = int(width * (1 - crop_percent))
        crop_h = int(height * (1 - crop_percent))
        start_x = random.randint(0, width - crop_w)
        start_y = random.randint(0, height - crop_h)
        img = img[start_y:start_y+crop_h, start_x:start_x+crop_w]
        
        # Resize back to original size
        img = cv2.resize(img, (width, height))
        
        # Apply scale
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, 0, scale_factor)
        img = cv2.warpAffine(img, rotation_matrix, (width, height))
        
        # Add Perlin noise (simplified version)
        noise = np.random.normal(0, noise_opacity * 255, img.shape).astype(np.uint8)
        img = cv2.addWeighted(img, 1.0, noise, noise_opacity, 0)
        
        # Apply color shifts in HLS space
        hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        hls[:,:,0] = np.clip(hls[:,:,0] + color_shift_h, 0, 179)  # H channel
        hls[:,:,1] = np.clip(hls[:,:,1] + color_shift_l, 0, 255)  # L channel
        hls[:,:,2] = np.clip(hls[:,:,2] + color_shift_s, 0, 255)  # S channel
        img = cv2.cvtColor(hls, cv2.COLOR_HLS2BGR)
        
        # Save result
        cv2.imwrite(output_path, img)
        
        return True
    
    def process_video(self, input_path, output_path, level):
        """Apply uniqueness enhancement to a video based on level"""
        # Get video info
        probe = ffmpeg.probe(input_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        duration = float(probe['format']['duration'])
        
        # Level-based parameters
        if level == 1:  # Low
            zoom_rate = 0.002  # 0.2% per second
            jitter_range = 1
            gop_size = 30
            crf = 22
        elif level == 2:  # Medium
            zoom_rate = 0.003  # 0.3% per second
            jitter_range = 1.5
            gop_size = 25
            crf = 21
        else:  # High
            zoom_rate = 0.005  # 0.5% per second
            jitter_range = 2
            gop_size = 20
            crf = 20
        
        # Build FFmpeg command with transformations
        input_video = ffmpeg.input(input_path)
        
        # Video transformations
        # Add zoom and pan drift
        zoom_filter = f"zoompan=z='min(zoom+{zoom_rate},1.2)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        
        # Add spatial jitter (simplified with noise)
        noise_filter = f"noise=alls={jitter_range}:allf=t+u"
        
        # Combine filters
        video_filters = f"{zoom_filter},{noise_filter}"
        
        # Audio transformations
        audio_input = input_video.audio if input_video.audio else None
        if audio_input:
            # Pitch shift and tempo compensation
            audio_processed = audio_input.filter('asetrate', 44100 * 1.023)  # +2.3% pitch
            audio_processed = audio_processed.filter('aresample', 44100)
            audio_processed = audio_processed.filter('atempo', 1.0/1.023)  # Compensate tempo
        else:
            audio_processed = None
        
        # Output with new encoding parameters
        output_kwargs = {
            'vcodec': 'libx264',
            'preset': 'medium',
            'crf': crf,
            'g': gop_size,
            'bf': 3,  # B-frames
            'movflags': '+faststart',
            'pix_fmt': 'yuv420p'
        }
        
        if audio_processed:
            output = ffmpeg.output(
                input_video.video.filter(video_filters),
                audio_processed,
                output_path,
                **output_kwargs
            )
        else:
            output = ffmpeg.output(
                input_video.video.filter(video_filters),
                output_path,
                **output_kwargs
            )
        
        # Run the command
        ffmpeg.run(output, overwrite_output=True, quiet=True)
        
        return True
    
    def analyze_video_uniqueness(self, original_path, processed_path):
        """Analyze video uniqueness by comparing keyframes and audio"""
        # Extract keyframes
        original_clip = VideoFileClip(original_path)
        processed_clip = VideoFileClip(processed_path)
        
        duration = min(original_clip.duration, processed_clip.duration)
        keyframe_times = np.linspace(0, duration, min(10, int(duration)))
        
        phash_differences = []
        for t in keyframe_times:
            try:
                orig_frame = original_clip.get_frame(t)
                proc_frame = processed_clip.get_frame(t)
                
                # Convert to PIL Images
                orig_pil = Image.fromarray(cv2.cvtColor(orig_frame, cv2.COLOR_BGR2RGB))
                proc_pil = Image.fromarray(cv2.cvtColor(proc_frame, cv2.COLOR_BGR2RGB))
                
                # Calculate phash
                orig_hash = imagehash.phash(orig_pil)
                proc_hash = imagehash.phash(proc_pil)
                
                # Calculate difference
                diff = orig_hash - proc_hash
                max_diff = len(orig_hash.hash) * orig_hash.hash.dtype.itemsize * 8
                percentage = (diff / max_diff) * 100
                phash_differences.append(percentage)
            except:
                continue
        
        avg_phash_diff = np.mean(phash_differences) if phash_differences else 0
        
        # Audio analysis if both clips have audio
        audio_similarity = 0
        if original_clip.audio and processed_clip.audio:
            try:
                # Extract audio and analyze
                orig_audio_path = os.path.join(self.temp_dir, "orig_audio.wav")
                proc_audio_path = os.path.join(self.temp_dir, "proc_audio.wav")
                
                original_clip.audio.write_audiofile(orig_audio_path, verbose=False, logger=None)
                processed_clip.audio.write_audiofile(proc_audio_path, verbose=False, logger=None)
                
                # Load audio for similarity comparison
                orig_audio, sr_orig = librosa.load(orig_audio_path)
                proc_audio, sr_proc = librosa.load(proc_audio_path)
                
                # Calculate spectrogram similarity
                orig_spec = librosa.stft(orig_audio[:min(len(orig_audio), len(proc_audio))])
                proc_spec = librosa.stft(proc_audio[:min(len(orig_audio), len(proc_audio))])
                
                # Calculate cosine similarity
                similarity = 1 - cosine(
                    np.abs(orig_spec).flatten(), 
                    np.abs(proc_spec).flatten()
                )
                audio_similarity = max(0, (1 - similarity) * 100)
                
                # Cleanup
                os.remove(orig_audio_path)
                os.remove(proc_audio_path)
            except:
                pass
        
        original_clip.close()
        processed_clip.close()
        
        return avg_phash_diff, audio_similarity
    
    def get_risk_level(self, phash_diff, audio_similarity=None):
        """Determine risk level based on uniqueness metrics"""
        if phash_diff >= 45:
            return "Низкий"
        elif phash_diff >= 30:
            return "Средний"
        else:
            return "Высокий"


class ProcessingThread:
    """Thread for processing media in background"""
    
    def __init__(self, processor, input_path, output_path, media_type, level, qt_modules=None):
        self.processor = processor
        self.input_path = input_path
        self.output_path = output_path
        self.media_type = media_type
        self.level = level
        self.qt_modules = qt_modules
        if qt_modules:
            self.pyqtSignal = qt_modules['pyqtSignal']
            self.progress = self.pyqtSignal(int)
            self.finished = self.pyqtSignal(str)  # Output path
    
    def run(self):
        try:
            if self.media_type == "image":
                self.processor.process_image(self.input_path, self.output_path, self.level)
            else:
                self.processor.process_video(self.input_path, self.output_path, self.level)
            
            if self.qt_modules:
                self.finished.emit(self.output_path)
        except Exception as e:
            print(f"Processing error: {e}")
            if self.qt_modules:
                self.finished.emit("")


class PreviewThread:
    """Thread for generating preview"""
    
    def __init__(self, processor, input_path, media_type, level, qt_modules=None):
        self.processor = processor
        self.input_path = input_path
        self.media_type = media_type
        self.level = level
        self.qt_modules = qt_modules
        if qt_modules:
            self.pyqtSignal = qt_modules['pyqtSignal']
            self.preview_ready = self.pyqtSignal(str)  # Preview path
    
    def run(self):
        try:
            preview_path = os.path.join(self.processor.temp_dir, "preview")
            if self.media_type == "image":
                preview_path += os.path.splitext(self.input_path)[1]
                self.processor.process_image(self.input_path, preview_path, self.level)
            else:
                preview_path += ".mp4"
                # Create a 3-second preview
                temp_preview = os.path.join(self.processor.temp_dir, "temp_preview.mp4")
                self.processor.process_video(self.input_path, temp_preview, self.level)
                
                # Extract first 3 seconds
                input_video = ffmpeg.input(temp_preview)
                output = ffmpeg.output(input_video, preview_path, t=3)
                ffmpeg.run(output, overwrite_output=True, quiet=True)
                
                os.remove(temp_preview)
            
            if self.qt_modules:
                self.preview_ready.emit(preview_path)
        except Exception as e:
            print(f"Preview generation error: {e}")
            if self.qt_modules:
                self.preview_ready.emit("")


class MainWindow:
    def __init__(self, qt_modules):
        self.qt_modules = qt_modules
        self.QApplication = qt_modules['QApplication']
        self.QMainWindow = qt_modules['QMainWindow']
        self.QWidget = qt_modules['QWidget']
        self.QVBoxLayout = qt_modules['QVBoxLayout']
        self.QHBoxLayout = qt_modules['QHBoxLayout']
        self.QPushButton = qt_modules['QPushButton']
        self.QLabel = qt_modules['QLabel']
        self.QSlider = qt_modules['QSlider']
        self.QFileDialog = qt_modules['QFileDialog']
        self.QProgressBar = qt_modules['QProgressBar']
        self.QTextEdit = qt_modules['QTextEdit']
        self.QGroupBox = qt_modules['QGroupBox']
        self.QRadioButton = qt_modules['QRadioButton']
        self.QButtonGroup = qt_modules['QButtonGroup']
        self.Qt = qt_modules['Qt']
        self.QThread = qt_modules['QThread']
        self.pyqtSignal = qt_modules['pyqtSignal']
        self.QPixmap = qt_modules['QPixmap']
        self.QDragEnterEvent = qt_modules['QDragEnterEvent']
        self.QDropEvent = qt_modules['QDropEvent']
        
        # Initialize the main window
        self.window = self.QMainWindow()
        self.window.setWindowTitle("Deep Media Uniqueness Enhancer")
        self.window.setGeometry(100, 100, 800, 600)
        
        self.processor = MediaProcessor()
        self.current_file = None
        self.media_type = None
        self.processed_file = None
        self.preview_file = None
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = self.QWidget()
        self.window.setCentralWidget(central_widget)
        layout = self.QVBoxLayout(central_widget)
        
        # Media type selector
        type_layout = self.QHBoxLayout()
        self.photo_radio = self.QRadioButton("📷 Фото")
        self.video_radio = self.QRadioButton("🎥 Видео")
        self.video_radio.setChecked(True)
        
        type_layout.addWidget(self.photo_radio)
        type_layout.addWidget(self.video_radio)
        layout.addLayout(type_layout)
        
        # File drop area
        self.drop_area = self.QLabel("Перетащите файл сюда или нажмите для выбора")
        self.drop_area.setAlignment(self.Qt.AlignmentFlag.AlignCenter)
        self.drop_area.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 10px;
                padding: 20px;
                font-size: 16px;
            }
        """)
        self.drop_area.mousePressEvent = self.select_file
        self.drop_area.setAcceptDrops(True)
        self.drop_area.dragEnterEvent = self.drag_enter_event
        self.drop_area.dropEvent = self.drop_event
        layout.addWidget(self.drop_area)
        
        # Uniqueness level
        level_group = self.QGroupBox("Уровень уникализации")
        level_layout = self.QHBoxLayout(level_group)
        
        self.level_slider = self.QSlider(self.Qt.Orientation.Horizontal)
        self.level_slider.setMinimum(1)
        self.level_slider.setMaximum(5)
        self.level_slider.setValue(3)
        self.level_slider.valueChanged.connect(self.update_level_label)
        
        self.level_label = self.QLabel("Средний (3/5)")
        level_layout.addWidget(self.level_slider)
        level_layout.addWidget(self.level_label)
        
        layout.addWidget(level_group)
        
        # Action buttons
        button_layout = self.QHBoxLayout()
        
        self.analyze_btn = self.QPushButton("Анализировать оригинал")
        self.analyze_btn.clicked.connect(self.analyze_original)
        self.analyze_btn.setEnabled(False)
        
        self.preview_btn = self.QPushButton("Сгенерировать preview")
        self.preview_btn.clicked.connect(self.generate_preview)
        self.preview_btn.setEnabled(False)
        
        self.export_btn = self.QPushButton("Экспортировать")
        self.export_btn.clicked.connect(self.export_media)
        self.export_btn.setEnabled(False)
        
        button_layout.addWidget(self.analyze_btn)
        button_layout.addWidget(self.preview_btn)
        button_layout.addWidget(self.export_btn)
        layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = self.QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Results panel
        self.results_panel = self.QTextEdit()
        self.results_panel.setMaximumHeight(150)
        self.results_panel.setReadOnly(True)
        layout.addWidget(self.results_panel)
        
        self.update_level_label()
    
    def update_level_label(self):
        level = self.level_slider.value()
        if level <= 2:
            text = f"Низкий ({level}/5)"
        elif level <= 3:
            text = f"Средний ({level}/5)"
        else:
            text = f"Высокий ({level}/5)"
        
        self.level_label.setText(text)
    
    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def drop_event(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.load_file(file_path)
    
    def select_file(self, event):
        file_path, _ = self.QFileDialog.getOpenFileName(
            self.window,
            "Выберите файл",
            "",
            "Media Files (*.jpg *.jpeg *.png *.webp *.mp4 *.mov *.avi *.mkv)"
        )
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        self.current_file = file_path
        self.media_type = "video" if file_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')) else "image"
        
        file_name = os.path.basename(file_path)
        self.drop_area.setText(f"Загружен: {file_name}")
        
        # Enable buttons
        self.analyze_btn.setEnabled(True)
        self.preview_btn.setEnabled(True)
        self.export_btn.setEnabled(True)
    
    def analyze_original(self):
        if not self.current_file:
            return
        
        self.results_panel.append("Анализ оригинала...")
        
        if self.media_type == "image":
            # Calculate image hash
            img = Image.open(self.current_file)
            phash = imagehash.phash(img)
            self.results_panel.append(f"Perceptual hash оригинала: {phash}")
        else:
            # For video, we can extract keyframes and analyze them
            clip = VideoFileClip(self.current_file)
            duration = clip.duration
            keyframe_time = min(3, duration / 2)  # Get middle frame or first 3 seconds
            
            try:
                frame = clip.get_frame(keyframe_time)
                pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                phash = imagehash.phash(pil_frame)
                self.results_panel.append(f"Perceptual hash кадра в {keyframe_time:.1f}s: {phash}")
                self.results_panel.append(f"Длительность видео: {duration:.2f} сек")
            except:
                self.results_panel.append("Ошибка при анализе видео")
            
            clip.close()
    
    def generate_preview(self):
        if not self.current_file:
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        self.preview_thread = PreviewThread(
            self.processor, 
            self.current_file, 
            self.media_type, 
            self.level_slider.value(),
            self.qt_modules
        )
        self.preview_thread.preview_ready.connect(self.preview_ready)
        # For compatibility with Nuitka, run in a separate thread
        import threading
        thread = threading.Thread(target=self.preview_thread.run)
        thread.start()
    
    def preview_ready(self, preview_path):
        self.progress_bar.setVisible(False)
        
        if preview_path and os.path.exists(preview_path):
            self.preview_file = preview_path
            self.results_panel.append(f"Preview готов: {os.path.basename(preview_path)}")
            
            if self.media_type == "image":
                # Show image preview
                pixmap = self.QPixmap(preview_path).scaled(200, 200, self.Qt.AspectRatioMode.KeepAspectRatio)
                self.drop_area.setPixmap(pixmap)
            else:
                self.results_panel.append("Видео preview сгенерирован")
        else:
            self.results_panel.append("Ошибка при генерации preview")
    
    def export_media(self):
        if not self.current_file:
            return
        
        # Choose output path
        output_ext = ".mp4" if self.media_type == "video" else os.path.splitext(self.current_file)[1]
        output_path, _ = self.QFileDialog.getSaveFileName(
            self.window,
            "Сохранить уникализированный файл",
            f"uniquified_{os.path.basename(self.current_file)}",
            f"Media Files (*{output_ext})"
        )
        
        if not output_path:
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        self.process_thread = ProcessingThread(
            self.processor,
            self.current_file,
            output_path,
            self.media_type,
            self.level_slider.value(),
            self.qt_modules
        )
        self.process_thread.finished.connect(self.processing_finished)
        # For compatibility with Nuitka, run in a separate thread
        import threading
        thread = threading.Thread(target=self.process_thread.run)
        thread.start()
    
    def processing_finished(self, output_path):
        self.progress_bar.setVisible(False)
        
        if output_path and os.path.exists(output_path):
            self.processed_file = output_path
            self.results_panel.append(f"Файл экспортирован: {os.path.basename(output_path)}")
            
            # Analyze uniqueness if we have both original and processed
            if self.media_type == "image":
                try:
                    diff = self.processor.calculate_phash_difference(self.current_file, output_path)
                    risk_level = self.processor.get_risk_level(diff)
                    self.results_panel.append(f"Различие phash: {diff:.2f}%")
                    self.results_panel.append(f"Уровень риска: {risk_level}")
                except:
                    self.results_panel.append("Ошибка при анализе уникальности")
            else:
                try:
                    phash_diff, audio_sim = self.processor.analyze_video_uniqueness(self.current_file, output_path)
                    risk_level = self.processor.get_risk_level(phash_diff, audio_sim)
                    self.results_panel.append(f"Различие phash кадров: {phash_diff:.2f}%")
                    self.results_panel.append(f"Аудио схожесть: {audio_sim:.2f}%")
                    self.results_panel.append(f"Уровень риска: {risk_level}")
                except:
                    self.results_panel.append("Ошибка при анализе видео уникальности")
        else:
            self.results_panel.append("Ошибка при обработке файла")
    
    def show(self):
        self.window.show()


def main():
    import sys
    # Check for CLI mode
    if "--cli" in sys.argv or "-c" in sys.argv:
        # CLI mode
        print("Deep Media Uniqueness Enhancer - CLI Mode")
        print("Usage: python main.py --cli <input_file> <output_file> <level>")
        print("Level: 1 (Low), 2 (Medium), 3 (High)")
        
        if len(sys.argv) >= 5:
            input_file = sys.argv[sys.argv.index("--cli") + 1] if "--cli" in sys.argv else sys.argv[sys.argv.index("-c") + 1]
            output_file = sys.argv[sys.argv.index("--cli") + 2] if "--cli" in sys.argv else sys.argv[sys.argv.index("-c") + 2]
            try:
                level = int(sys.argv[sys.argv.index("--cli") + 3]) if "--cli" in sys.argv else int(sys.argv[sys.argv.index("-c") + 3])
            except (ValueError, IndexError):
                level = 3  # Default to medium
            
            print(f"Processing: {input_file}")
            print(f"Output: {output_file}")
            print(f"Level: {level}")
            
            processor = MediaProcessor()
            media_type = "video" if input_file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')) else "image"
            
            if media_type == "image":
                processor.process_image(input_file, output_file, level)
            else:
                processor.process_video(input_file, output_file, level)
            
            print("Processing completed!")
        else:
            print("Not enough arguments for CLI mode")
    else:
        # GUI mode
        try:
            qt_modules = get_qt_modules()
            app = qt_modules['QApplication'](sys.argv)
            window = MainWindow(qt_modules)
            window.show()
            sys.exit(app.exec())
        except ImportError as e:
            print(f"GUI mode requires PyQt6: {e}")
            print("Install with: pip install PyQt6")
            sys.exit(1)


if __name__ == "__main__":
    main()