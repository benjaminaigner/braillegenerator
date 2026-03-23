# Setup and Installation Guide

## System Requirements

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 50 MB free disk space

## Installation Steps

### 1. Clone or Download the Repository

```bash
cd braillegenerator
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install Flask==2.3.0
pip install Flask-CORS==4.0.0
```

### 3. Start the Server

**On Windows:**
```bash
python server.py
```

**On macOS/Linux:**
```bash
python3 server.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 4. Access the Web Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### Using the Web GUI

1. **Enter Text**: Type or paste your text in the "Braille Text" field
   - You can enter multiple lines
   - The text will be converted to German braille

2. **Select Page Size**: Choose from preset sizes or custom dimensions
   - **A5 (148×210mm)**: Standard note card size
   - **A6 (105×148mm)**: Postcard size
   - **A7 (74×105mm)**: Small format
   - **B5 (176×250mm)**: Large format
   - **Custom**: Set your own width and height

3. **Configure Plates**:
   - **Include Back Plate**: Adds a 2mm thickness for rigidity (recommended)
   - **Include Support Plates**: Adds stabilizing supports (recommended for printing)

4. **Generate Model**:
   - Click "Generate 3D Model"
   - Wait for the preview to appear (usually 1-5 seconds)
   - Examine your model in the 3D preview
   - Rotate: Drag your mouse
   - Zoom: Use mouse wheel

5. **Download**:
   - Once satisfied, click "⬇ Download STL"
   - The STL file will be downloaded to your default download folder

### 3D Printing Tips

1. **Orientation**: Print with the back plate down
2. **Support**: If enabled, the support plates will prevent warping
3. **Layer Height**: Use 0.2mm for balanced quality and speed
4. **Infill**: 20% is usually sufficient
5. **Material**: PLA or PETG work well for braille plates
6. **Post-processing**: Sand lightly if needed for smoother dots

### Using with OpenJSCAD Online

If you prefer not to run the server, you can use the web-based OpenJSCAD editor:

1. Go to https://joostn.github.io/OpenJsCad/processfile.html
2. Load the `braille.jscad` file
3. Adjust parameters in the web interface
4. Export as STL

## Troubleshooting

### Port Already in Use

If you see "Address already in use":
```bash
# Change the port in server.py (last line: app.run(port=5001))
# Or kill the process using port 5000:

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti :5000 | xargs kill -9
```

### File Not Found Error

Ensure `braille.jscad` is in the same directory as `server.py`

### STL File Not Downloading

Try:
1. Clear browser cache
2. Disable ad blockers
3. Try a different browser
4. Check browser's download settings

## Performance Notes

- File generation typically takes 1-5 seconds
- File sizes typically range from 100KB to 2MB depending on text length
- Larger text or smaller page sizes may take slightly longer

## Advanced Configuration

Edit `server.py` to modify:

```python
# Change server port (default: 5000)
app.run(port=5001)

# Enable/disable debug mode
app.run(debug=False)

# Change host (default: localhost only)
app.run(host='0.0.0.0')
```

## File Structure

```
braillegenerator/
├── braille.jscad          # Core 3D model file
├── server.py              # Flask backend
├── index.html             # Web interface
├── requirements.txt       # Python dependencies
├── README.md              # Main documentation
└── INSTALLATION.md        # This file
```

## Support

For issues or feature requests, check the GitHub repository or create an issue.

Happy printing!
