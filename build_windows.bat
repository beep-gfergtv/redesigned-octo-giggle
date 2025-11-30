@echo off
echo Building Media Uniqueness Enhancer for Windows...
echo.

REM Install Nuitka if not already installed
pip install nuitka

echo.
echo Building GUI version (without console)...
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-disable-console ^
    --windows-company-name="Media Enhancer" ^
    --windows-product-name="Media Uniqueness Enhancer" ^
    --windows-file-version=1.0.0 ^
    --windows-product-version=1.0.0 ^
    --include-data-file=README.md=README.md ^
    --include-data-file=requirements.txt=requirements.txt ^
    --include-package=PyQt6 ^
    --include-package=PyQt6.QtCore ^
    --include-package=PyQt6.QtGui ^
    --include-package=PyQt6.QtWidgets ^
    --include-package=cv2 ^
    --include-package=imagehash ^
    --include-package=numpy ^
    --include-package=PIL ^
    --include-package=moviepy ^
    --include-package=librosa ^
    --include-package=librosa.core ^
    --include-package=librosa.feature ^
    --include-package=librosa.util ^
    --include-package=librosa.effects ^
    --include-package=ffmpeg ^
    --include-package=ffmpeg_python ^
    --include-package=scipy ^
    --include-package=scipy.spatial ^
    --include-package=scipy.linalg ^
    --include-package=tqdm ^
    --remove-output ^
    --output-filename=MediaUniquenessEnhancer.exe ^
    main.py

echo.
echo Building CLI version (with console)...
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-company-name="Media Enhancer" ^
    --windows-product-name="Media Uniqueness Enhancer CLI" ^
    --windows-file-version=1.0.0 ^
    --windows-product-version=1.0.0 ^
    --include-data-file=README.md=README.md ^
    --include-data-file=requirements.txt=requirements.txt ^
    --include-package=PyQt6 ^
    --include-package=PyQt6.QtCore ^
    --include-package=PyQt6.QtGui ^
    --include-package=PyQt6.QtWidgets ^
    --include-package=cv2 ^
    --include-package=imagehash ^
    --include-package=numpy ^
    --include-package=PIL ^
    --include-package=moviepy ^
    --include-package=librosa ^
    --include-package=librosa.core ^
    --include-package=librosa.feature ^
    --include-package=librosa.util ^
    --include-package=librosa.effects ^
    --include-package=ffmpeg ^
    --include-package=ffmpeg_python ^
    --include-package=scipy ^
    --include-package=scipy.spatial ^
    --include-package=scipy.linalg ^
    --include-package=tqdm ^
    --remove-output ^
    --output-filename=MediaUniquenessEnhancer_CLI.exe ^
    main.py

echo.
echo Build completed! Check the .exe files in the current directory.
pause