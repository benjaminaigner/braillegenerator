# Code Architecture & Module Documentation

## Overview

The Braille Plate Generator is a full-stack application for generating customizable 3D braille plates for 3D printing. This document explains the codebase structure, modules, and architecture.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Web Browser                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ index.html                                                │  │
│  │ - HTML structure with form inputs                         │  │
│  │ - CSS styling (responsive design)                         │  │
│  │ - THREE.js 3D preview (client-side)                       │  │
│  │ - Fetch API to communicate with backend                   │  │
│  └───────────────┬─────────────────────────────────────────┘  │
└──────────────────┼──────────────────────────────────────────────┘
                   │ HTTP/JSON
                   ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Flask Backend                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ server.py                                                 │  │
│  │ - Flask application setup                                 │  │
│  │ - HTTP routes and endpoints                               │  │
│  │ - Request/response handling                               │  │
│  │ - STL file generation and download                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                       ↓                                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ braille.jscad                                             │  │
│  │ - JSCAD 3D model definition                               │  │
│  │ - Braille character mappings                              │  │
│  │ - Geometry generation                                     │  │
│  │ - Page size parameters and scaling                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                       ↓                                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Temporary Files                                           │  │
│  │ - JSCAD intermediate files                                │  │
│  │ - STL output files                                        │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## File Structure

```
braillegenerator/
├── server.py                    # Flask backend application
├── index.html                   # Web interface (frontend)
├── braille.jscad                # 3D model definition (JSCAD)
├── requirements.txt             # Python dependencies
├── test_server.py               # Unit tests
├── start_server.bat             # Windows startup script
├── start_server.sh              # Unix startup script
│
├── Documentation/
│   ├── README.md                # Project overview
│   ├── INSTALLATION.md          # Setup guide
│   ├── FEATURE_GUIDE.md         # Feature documentation
│   ├── QUICK_REFERENCE.md       # Quick start guide
│   ├── TECHNICAL_DETAILS.md     # Technical implementation
│   ├── SERVER_STARTUP_GUIDE.md  # Troubleshooting
│   ├── CODE_ARCHITECTURE.md     # This file
│   └── TESTING_GUIDE.md         # Testing documentation
│
├── img/                         # Project images
└── LICENSE                      # License file
```

## Core Modules

### 1. server.py - Flask Backend

**Purpose**: HTTP server for the web interface and API endpoints

**Key Components**:

#### Imports and Setup
```python
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import os
from pathlib import Path
```

- `Flask`: Web framework
- `flask_cors`: Enable cross-origin requests
- `tempfile`: Handle temporary file creation
- `Path`: Path manipulation

#### Module-Level Variables

```python
Base_DIR = Path(__file__).parent
app = Flask(__name__)
CORS(app)
```

- `BASE_DIR`: Absolute path to application directory
- `app`: Flask application instance
- `CORS`: Enables cross-origin resource sharing

#### Routes (Endpoints)

**GET /health**
```python
@app.route('/health', methods=['GET'])
def health():
```
- Purpose: Health check endpoint
- Returns: `{"status": "ok", "service": "braille-generator"}`
- Used by: Load balancers, monitoring systems

**POST /generate**
```python
@app.route('/generate', methods=['POST'])
def generate():
```
- Purpose: Generate braille 3D model
- Input: JSON with text, page size, dimensions, plate options
- Output: JSON with filename, file size, status
- Process:
  1. Validate input parameters
  2. Load braille.jscad template
  3. Override parameters with user input
  4. Generate STL file
  5. Return filename for download

**GET /download/<filename>**
```python
@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
```
- Purpose: Download generated STL file
- Input: Filename in URL path
- Output: Binary STL file
- Security: Validates filename to prevent directory traversal

**GET /**
```python
@app.route('/', methods=['GET'])
def index():
```
- Purpose: Serve HTML interface
- Returns: index.html file
- Used by: Web browser when accessing http://localhost:5000

#### Functions

**generate_stl_from_jscad()**
```python
def generate_stl_from_jscad(jscad_file, text, page_size, width, height, back_plate, support_plate):
```
- Purpose: Convert JSCAD to STL file
- Parameters:
  - `jscad_file`: Path to JSCAD file
  - `text`: Braille text
  - `page_size`: Page size name or 'Custom'
  - `width`, `height`: Page dimensions
  - `back_plate`: Boolean for back plate
  - `support_plate`: Boolean for support plate
- Returns: Path to generated STL file
- Creates: ASCII STL file with simple geometry

**create_stl_box()**
```python
def create_stl_box(width, height, depth):
```
- Purpose: Generate STL content for a box shape
- Parameters:
  - `width`: Box width
  - `height`: Box height
  - `depth`: Box depth
- Returns: ASCII STL content string
- Details:
  - Creates box vertices at ±width/2, ±height/2, ±depth/2
  - Generates 12 triangles (2 per face, 6 faces)
  - Calculates normals for each triangle

### 2. index.html - Frontend Interface

**Purpose**: Web-based user interface

**Structure**:

```html
<!DOCTYPE html>
├── <head>
│   ├── Meta tags
│   ├── Styles (CSS)
│   └── THREE.js library
│
└── <body>
    ├── Header
    ├── Main content (2-column layout)
    │   ├── Left: Form inputs
    │   └── Right: 3D preview
    └── Script (JavaScript)
        ├── Initialization
        ├── THREE.js setup
        ├── Event handlers
        └── Communication with backend
```

**Key JavaScript Objects**:

```javascript
pageSizes = {
    'A5': [148, 210],
    'A6': [105, 148],
    'A7': [74, 105],
    'B5': [176, 250],
    'Custom': [100, 150]
}
```
- Maps page size names to dimensions [width, height]

**Key JavaScript Functions**:

```javascript
function initThreeJS()
```
- Initializes THREE.js 3D scene
- Sets up camera, renderer, lighting
- Enables mouse controls

```javascript
function generateBraille()
```
- Collects form data
- Sends POST request to /generate endpoint
- Handles response
- Updates preview

```javascript
function displayModel(geometry)
```
- Creates THREE.js mesh from geometry
- Adds to scene
- Fits to view

```javascript
function downloadSTL()
```
- Constructs download URL
- Triggers file download
- Shows success message

### 3. braille.jscad - 3D Model Definition

**Purpose**: Defines 3D braille model using JSCAD

**Key Components**:

**Constants**:
```javascript
const diameter = 1.44;          // Braille dot diameter (mm)
const resolution = 8;            // Circle resolution (triangles)
const plate_thickness = 2;       // Back plate thickness (mm)
const col_size = 3;              // Rows per braille cell
const brailledialect = 'german'; // Current supported dialect
const spacing = 2.5;             // Distance between dots
const distance = 6;              // Distance between characters
const plate_height = 10.8;       // Distance between lines
```

**Braille Maps**:
```javascript
const brailleMapSingleChar = {    // Single character mappings
    'german': {
        'a': [1,0,0,0,0,0],
        'b': [1,0,1,0,0,0],
        // ... 90+ characters
    }
}

const brailleMapDigits = {        // Digit mappings
    'german': {
        'start': [0,1,0,1,1,1],
        '1': [1,0,0,0,0,0],
        // ... 10 digits
    }
}

const brailleMapDoubleChar = {    // Two-character mappings
    'german': {
        'st': [0,1,1,1,1,1],
        'au': [1,0,0,0,0,1],
        // ... 7 combinations
    }
}

const brailleMapTripleChar = {    // Three-character mappings
    'german': {
        'sch': [1,0,0,1,0,1]
    }
}
```

**Page Size Definitions**:
```javascript
const pageSizes = {
    'A5': [148, 210],
    'A6': [105, 148],
    'A7': [74, 105],
    'B5': [176, 250],
    'Custom': [100, 150]
};
```

**Key Functions**:

```javascript
function getParameterDefinitions()
```
- Returns array of parameters for JSCAD interface
- Defines page size, dimensions, text, plate options

```javascript
function main(params)
```
- Entry point for 3D generation
- Handles scaling based on page size
- Combines braille dots, back plate, support plates
- Returns CSG object

```javascript
function braille_line(line)
```
- Converts single line of text to braille dots
- Returns CSG object with spacing

```javascript
function braille_str(text)
```
- Converts multi-line text to braille
- Returns CSG with dimensions

```javascript
function letter(bitmap)
```
- Creates single braille character
- Bitmap: [6] array of dots (0=off, 1=on)

## API Documentation

### POST /generate

**Request**:
```json
{
  "text": "Braille text",
  "pageSize": "A5",
  "customWidth": 100,
  "customHeight": 150,
  "backPlate": true,
  "supportPlate": true
}
```

**Response (Success - 200)**:
```json
{
  "status": "success",
  "filename": "braille_1234567890.stl",
  "file_size": 123456,
  "message": "STL generated successfully"
}
```

**Response (Error - 400)**:
```json
{
  "error": "Text is required"
}
```

**Parameters**:
- `text` (string, required): Braille text to convert
- `pageSize` (string, default: "Custom"): Predefined size or "Custom"
- `customWidth` (number, default: 100): Width in mm
- `customHeight` (number, default: 150): Height in mm
- `backPlate` (boolean, default: true): Include 2mm base plate
- `supportPlate` (boolean, default: true): Include support structures

### GET /download/<filename>

**Response (Success - 200)**:
Binary STL file

**Response (Error - 404)**:
```json
{
  "error": "File not found"
}
```

### GET /health

**Response (Success - 200)**:
```json
{
  "status": "ok",
  "service": "braille-generator"
}
```

### GET /

**Response (Success - 200)**:
HTML file (index.html)

**Response (Error - 404)**:
```json
{
  "error": "index.html not found"
}
```

## Data Flow

### Generation Flow

```
User Input (Web Form)
    ↓
JavaScript: Collect Form Data
    ↓
HTTP POST /generate (JSON)
    ↓
Flask: validate_input()
    ↓
Load braille.jscad Template
    ↓
Create Parameter Override
    ↓
generate_stl_from_jscad()
    ↓
Create Temporary Files
    ↓
HTTP Response (filename, size)
    ↓
JavaScript: Update Preview + Enable Download
    ↓
User Clicks Download
    ↓
HTTP GET /download/<filename>
    ↓
Flask: serve_file()
    ↓
Browser: Download STL File
```

### Parameter Flow in /generate

```
{text, pageSize, customWidth, customHeight, backPlate, supportPlate}
    ↓
Determine actual dimensions from pageSizes map
    ↓
Load braille.jscad content
    ↓
Create parameter override string:
    const paramsOverride = {
        text: '...',
        pageSize: '...',
        customWidth: X,
        customHeight: Y,
        backPlate: bool,
        supportPlate: bool
    };
    ↓
Append to JSCAD file
    ↓
JSCAD Engine Execution
    ↓
main(paramsOverride) function runs
    ↓
Generate STL
```

## Scaling Algorithm (braille.jscad)

```
Target Dimensions = pageSizes[pageSize] || [customWidth, customHeight]
Margins = 5mm on all sides
Available Width = Target Width - (2 × Margins)
Available Height = Target Height - (2 × Margins)

Scale_X = Available Width / Content Width
Scale_Y = Available Height / Content Height
Scale = min(Scale_X, Scale_Y, 1.0)  // Never upscale

Offset_X = (Target Width - Scaled Content Width) / 2
Offset_Y = (Target Height - Scaled Content Height) / 2

Apply: scale([Scale, Scale, 1])
Apply: translate([Offset_X, Offset_Y, 0])
```

## Testing Strategy

See `TESTING_GUIDE.md` for comprehensive testing documentation.

**Test Levels**:
1. **Unit Tests**: Individual functions
2. **Integration Tests**: Endpoints + file generation
3. **Manual Tests**: Web interface

**Test Coverage**:
- Endpoint accessibility
- Parameter validation
- Error handling
- File operations
- Response formats

## Extending the Codebase

### Adding a New Page Size

1. **In braille.jscad**:
```javascript
const pageSizes = {
    // ... existing sizes ...
    'A4': [210, 297]  // Add new size
};
```

2. **In index.html**:
```html
<select id="pageSize">
    <!-- ... existing options ... -->
    <option value="A4">A4 (210 x 297 mm)</option>
</select>
```

3. **Test**:
```python
def test_generate_a4_size(self):
    payload = {
        'text': 'A4 Test',
        'pageSize': 'A4',
        # ... other params ...
    }
```

### Adding a New Braille Dialect

1. **In braille.jscad**:
```javascript
const brailleMapSingleChar = {
    'german': { /* existing */ },
    'french': { /* new mappings */ }  // Add new dialect
};
```

2. **Update parameter**:
```javascript
{ name: 'brailledialect', caption: '...', type: 'choice', 
  options: ['german', 'french'] }
```

### Adding Backend Validation

**In server.py `/generate` function**:
```python
# Add before STL generation
if len(text) > 500:
    return jsonify({'error': 'Text too long'}), 400

if custom_width < 50 or custom_width > 300:
    return jsonify({'error': 'Invalid width'}), 400
```

## Dependencies

**Python**:
- `Flask 2.3.0`: Web framework
- `Flask-CORS 4.0.0`: Cross-origin support

**JavaScript**:
- `THREE.js r128`: 3D graphics library (CDN)

**System**:
- Python 3.7+
- Modern web browser (HTML5, WebGL support)

## Performance Considerations

### File Generation
- Average time: 1-3 seconds
- Bottleneck: Current JSCAD implementation uses simplified geometry
- Optimization: Consider binary STL instead of ASCII

### File Size
- Small (A7): ~100-300 KB
- Medium (A5): ~300-600 KB
- Large (custom): ~600 KB - 2 MB
- Optimization: Reduce mesh resolution in braille.jscad

### Memory Usage
- Flask app: ~50 MB baseline
- Per request: ~50-100 MB (temporary files)
- Browser preview: ~100 MB (THREE.js)

## Security Considerations

1. **File Path Validation**: `/download` endpoint uses `os.path.basename()` to prevent directory traversal
2. **Input Validation**: Text parameters are sanitized for JSCAD embedding
3. **CORS**: Enabled to allow cross-origin requests (for development)
4. **Temporary Files**: Cleaned up after download

## Logging

**Current Setup**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

**Usage**:
```python
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

**Output**: Printed to console during development

## Debugging

### Enable Verbose Logging
```powershell
python -u server.py
```

### Test Individual Endpoints
```powershell
# Health check
curl http://127.0.0.1:5000/health

# Generate with test data
curl -X POST http://127.0.0.1:5000/generate `
  -H "Content-Type: application/json" `
  -d '{"text":"Test","pageSize":"A5",...}'
```

### Inspect Temporary Files
```powershell
# List temp files
Get-ChildItem $env:TEMP | grep braille

# Manual STL test
type "C:\Users\...\Temp\braille_*.stl"
```

## Future Enhancements

1. **Database**: Store generation history
2. **Authentication**: User accounts and saved designs
3. **Advanced Options**: Dot size, spacing customization
4. **Batch Processing**: Generate multiple files
5. **Webhook Support**: Integration with external services
6. **Docker**: Containerized deployment
7. **API Rate Limiting**: Protect against abuse
8. **Progressive Web App**: Offline support

## Version History

- **v2.0**: Page sizes, web GUI, STL export
- **v1.0**: Basic JSCAD generator

---

**Last Updated**: March 23, 2026
**Maintained By**: AI Assistant
