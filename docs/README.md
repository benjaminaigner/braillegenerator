# Braille Plate Generator

A comprehensive system for generating 3D braille plates for 3D printing. Features a modern web GUI, customizable page sizes (A5, A6, A7, B5, or custom), and easy STL export.

## ✨ New Features

- **Page Size Presets**: Quickly select standard page sizes (A5, A6, A7, B5) or enter custom dimensions
- **Modern Web GUI**: Beautiful, user-friendly interface for generating braille plates
- **Real-time 3D Preview**: View your model before exporting
- **Easy STL Export**: One-click download of your generated model in STL format
- **Responsive Design**: Works on desktop and mobile devices
- **Multi-line Support**: Enter multiple lines of text with automatic formatting

## 🚀 Quick Start

### Web GUI (Recommended)

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   python server.py
   ```

3. Open your browser and go to `http://localhost:5000`

4. Enter your text, select page size, and click "Generate 3D Model"

5. Download the STL file for 3D printing

### Direct OpenJSCAD Usage

You can also use the enhanced `braille.jscad` file directly:
* Use the OpenJSCAD parser: https://joostn.github.io/OpenJsCad/processfile.html
* Upload the `braille.jscad` file and adjust parameters

## 📋 Parameters

### Text
- Enter any text you want to convert to braille
- Use newlines (`\n`) for multiple lines
- Supports German braille encoding

### Page Size
- **A5**: 148 × 210 mm (standard note card)
- **A6**: 105 × 148 mm (small postcard)
- **A7**: 74 × 105 mm (very small)
- **B5**: 176 × 250 mm (large format)
- **Custom**: Define your own width and height

### Plate Options
- **Back Plate**: 2mm support plate for stability (recommended for 3D printing)
- **Support Plates**: Additional support structures to prevent warping during printing

## 📐 Sizing

The generator automatically scales your braille text to fit within the selected page size with:
- Automatic scaling to maintain readability
- 5mm margins on all sides
- Proportional scaling to prevent distortion

# Original Project

Based on the OpenJSCAD braille generator:
- Original project: https://github.com/benjaminaigner/braillegenerator
- OpenJSCAD: https://github.com/joostn/OpenJsCad

## License

See LICENSE file for details.

