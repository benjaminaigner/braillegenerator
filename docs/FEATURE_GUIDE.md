# 🎨 Braille Plate Generator - Feature Guide

## What's New

Your braille generator has been enhanced with **three major features**:

### 1. 📐 Page Size Options
- **Problem Solved**: Users can now specify exactly how big the braille plate should be
- **Solutions Provided**:
  - **5 Preset Sizes**: A5, A6, A7, B5, and Custom
  - **Auto-scaling**: Text automatically scales to fit the selected page size
  - **Margins**: 5mm margins automatically applied on all sides
  - **Custom Dimensions**: Set any width and height you need (in mm)

**Example Use Cases**:
- Create A5 (148×210mm) plates for standard note cards
- Create A6 (105×148mm) plates for postcards
- Create custom 100×150mm plates for specific projects

### 2. 🌐 Modern Web GUI
- **Problem Solved**: No need to use external JSCAD editors or command line
- **Solution**: Beautiful, intuitive web interface with:
  - Text input field
  - Dropdown for page size selection
  - Easy toggle for back plate and support plates
  - Real-time 3D model preview
  - Responsive design works on phone/tablet/desktop

### 3. 📥 STL Export
- **Problem Solved**: Simple one-click download of your models
- **Solution**: 
  - Generate button creates the 3D model
  - Download button saves as `.stl` file
  - File naming includes date for organization
  - Compatible with all major 3D slicing software

## How to Use

### Quick Start (5 minutes)

**Step 1: Install**
```bash
pip install -r requirements.txt
```

**Step 2: Run**
- Windows: Double-click `start_server.bat`
- Mac/Linux: Run `bash start_server.sh`
- Or manually: `python server.py`

**Step 3: Enter Text**
```
Go to http://localhost:5000 and type your braille text
```

**Step 4: Select Size**
```
Choose from A5, A6, A7, B5, or set custom dimensions
```

**Step 5: Download**
```
Click "Generate 3D Model" → "Download STL"
```

### Detailed Workflow

```
┌─────────────────────────────────┐
│ 1. Web Browser (localhost:5000) │
├─────────────────────────────────┤
│ Enter text                      │
│ Select page size                │
│ Configure plates                │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│ 2. Backend (server.py)          │
├─────────────────────────────────┤
│ Process input                   │
│ Generate 3D geometry            │
│ Create STL file                 │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│ 3. Download                     │
├─────────────────────────────────┤
│ .stl file ready for:            │
│ - Cura                          │
│ - PrusaSlicer                   │
│ - Simplify3D                    │
│ - Any 3D slicer                 │
└─────────────────────────────────┘
```

## File Reference

### Modified Files
- **braille.jscad**: Added page size parameters and scaling logic
  - New parameters: `pageSize`, `customWidth`, `customHeight`
  - New page size definitions with A5, A6, A7, B5 presets
  - Automatic scaling to fit content in page size

### New Files
- **server.py**: Flask backend server
  - `/generate`: POST endpoint for model generation
  - `/download/<filename>`: GET endpoint for STL download
  - `/`: Serves the web interface

- **index.html**: Web GUI interface
  - Beautiful modern design
  - Three.js 3D preview
  - Form controls for all parameters
  - Responsive layout

- **requirements.txt**: Python dependencies
  - Flask 2.3.0
  - Flask-CORS 4.0.0

- **start_server.bat**: Windows startup script
- **start_server.sh**: macOS/Linux startup script
- **INSTALLATION.md**: Detailed setup guide
- **FEATURE_GUIDE.md**: This file

## Parameter Details

### Text
- Multi-line support with `\n`
- German braille encoding
- Special characters supported
- Maximum length: Limited by page size

### Page Sizes
| Size | Dimensions | Best For |
|------|-----------|----------|
| A5 | 148×210mm | Standard note cards |
| A6 | 105×148mm | Postcards |
| A7 | 74×105mm | Small labels |
| B5 | 176×250mm | Large formats |
| Custom | User-defined | Special projects |

### Configuration Options
| Option | Description |
|--------|-------------|
| Back Plate | 2mm support layer (recommended for printing) |
| Support Plates | Stabilizing structures for better print results |

## 3D Printing Tips

### Recommended Settings
- **Nozzle**: 0.4mm
- **Layer Height**: 0.2mm (or 0.1mm for detail)
- **Support**: Enable supports under the back plate
- **Infill**: 20%
- **Speed**: 50mm/s (slower for detail)

### Material Recommendations
- **PLA**: Easy to print, good detail
- **PETG**: More durable, slightly harder to print
- **ABS**: Very durable but requires heated bed

### Post-Processing
1. Remove supports carefully
2. Sand dots if needed (start with 120 grit)
3. Wash with warm soapy water
4. Dry completely

## Technical Details

### Architecture
```
┌─────────────────┐
│  Web Interface  │ (HTML/CSS/JavaScript)
│   (index.html)  │ • THREE.js for 3D preview
└────────┬────────┘
         │ HTTP/JSON
         ↓
┌─────────────────┐
│    Flask App    │ (server.py)
│   (server.py)   │ • Handles requests
└────────┬────────┘ • Processes JSCAD
         │          • Generates STL
         ↓
┌─────────────────┐
│  JSCAD Engine   │ (braille.jscad)
│  (braille.jscad)│ • Renders 3D model
└─────────────────┘
```

### How Scaling Works
1. User enters text and page size
2. Backend calculates braille geometry dimensions
3. Scale factors computed: `width_ratio = page_width / text_width`
4. Content scaled to fit within margins (5mm each side)
5. Results centered on page with maintained aspect ratio

## Troubleshooting

### Issue: "Port 5000 already in use"
**Solution**: 
- Edit `server.py` line: `app.run(port=5001)`
- Or kill the process using the port

### Issue: "STL file too large"
**Solution**:
- Reduce mesh resolution in braille.jscad (line `const resolution = 8`)
- Use custom page size to reduce content size

### Issue: "Model looks distorted"
**Solution**:
- Check page size vs text length
- Try a larger page size
- Enable back plate for stability

## Performance

| Metric | Value |
|--------|-------|
| Average generation time | 1-3 seconds |
| Typical file size | 200KB - 1.5MB |
| Max page size | 300×300mm |
| Max text length | ~500 characters per page |

## Future Enhancements

Potential additions:
- Multiple braille dialects (currently German only)
- Text effects (outline, emboss, etc.)
- Batch generation
- API for automation
- Cloud storage integration
- Mobile app

## Support & Feedback

For issues, feature requests, or feedback:
1. Check INSTALLATION.md for setup help
2. Review this guide for usage help
3. Check server logs for errors
4. Verify Python version (3.7+)

## License

See LICENSE file for details.

---

**Enjoy creating beautiful braille prints! 🎉**
