PIXELLAB - PYTHON GUI (VERSION 2)

Requirements:
- Python 3.10+
- Windows / macOS / Linux with a desktop environment

Setup:
1. Extract the ZIP file.
2. Open the extracted folder in VS Code.
3. Open Terminal in the project folder.
4. Run:
       pip install -r requirements.txt
5. Start the GUI:
       python main.py

Features:
- CustomTkinter graphical interface.
- Supplied cosmic image used as the background.
- Upload PNG, JPG, JPEG, WEBP and BMP.
- RGB to Grayscale.
- Grayscale to Binary with adjustable threshold.
- RGB to CMY and CMYK.
- Negative, Sepia, Blur, Sharpen and Edge Detection.
- Original and converted image previews.
- Download converted image.
- Offline demo image and Reset button.

Files:
main.py
requirements.txt
assets/pixellab_background.jpg

Technical notes:
- CMY is calculated as C=255-R, M=255-G, Y=255-B.
- CMYK is calculated by Pillow's image color conversion. The result is
  converted to RGB for the GUI preview. If you need a CMYK output file
  for print, we can add a separate CMYK export option.
- The current app uses a file picker. Drag-and-drop can be added with
  tkinterdnd2 if the project requirements permit an extra dependency.
