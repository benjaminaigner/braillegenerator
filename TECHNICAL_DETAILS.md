# Technical Implementation - Code Changes

## Overview

The braille plate generator has been enhanced with three main improvements:

## 1. Page Size Parameters (braille.jscad)

### What Changed

#### Old Code:
```javascript
function getParameterDefinitions() {
  return [
    { name: 'supportPlate', caption: '...' },
    { name: 'backPlate', caption: '...' },
    { name: 'text', caption: '...' },
  ];
}
```

#### New Code:
```javascript
function getParameterDefinitions() {
  return [
    { name: 'text', caption: 'Braille Text:', ... },
    { name: 'pageSize', caption: 'Seitengröße:', type: 'choice', 
      options: ['Custom', 'A5', 'A6', 'A7', 'B5'] },
    { name: 'customWidth', caption: 'Breite (mm)...', type: 'float' },
    { name: 'customHeight', caption: 'Höhe (mm)...', type: 'float' },
    { name: 'backPlate', caption: '...' },
    { name: 'supportPlate', caption: '...' },
  ];
}
```

### Added Page Size Definitions
```javascript
const pageSizes = {
  'A5': [148, 210],
  'A6': [105, 148],
  'A7': [74, 105],
  'B5': [176, 250],
  'Custom': [100, 150]
};
```

**Page size standards (ISO 216)**:
- A5: Half of A4 (commonly used for note cards)
- A6: Half of A5 (postcard size)
- A7: Half of A6 (small labels)
- B5: Between A4 and A5 (large format)

## 2. Scaling Algorithm (main function)

### Key Addition: Automatic Scaling

```javascript
function main(params) {
    // Determine target dimensions
    var targetWidth, targetHeight;
    if (params.pageSize === 'Custom') {
        targetWidth = params.customWidth;
        targetHeight = params.customHeight;
    } else {
        var sizeArray = pageSizes[params.pageSize];
        targetWidth = sizeArray[0];
        targetHeight = sizeArray[1];
    }
    
    // Calculate scale to fit content
    const marginX = 5;  // 5mm margin
    const marginY = 5;
    const maxContentWidth = targetWidth - (2 * marginX);
    const maxContentHeight = targetHeight - (2 * marginY);
    
    // Calculate scale factors
    const scaleX = maxContentWidth / width;
    const scaleY = maxContentHeight / height;
    const scale = Math.min(scaleX, scaleY, 1);  // Don't upscale
    
    // Apply scaling
    finalobject = finalobject.scale([scale, scale, 1]);
}
```

### How It Works

1. **Get Target Size**: Read page size or use custom dimensions
2. **Calculate Available Space**: Subtract margins from page size
3. **Calculate Scale Ratio**: Determine how much to scale content
4. **Limit Upscaling**: Never scale above 1.0 (quality preservation)
5. **Center Content**: Calculate offset to center braille text
6. **Apply Transformation**: Scale and translate the geometry

### Mathematical Formula

```
Scale = min(
    (PageWidth - 2×Margin) / ContentWidth,
    (PageHeight - 2×Margin) / ContentHeight,
    1.0
)

Offset_X = (PageWidth - ScaledContentWidth) / 2
Offset_Y = (PageHeight - ScaledContentHeight) / 2
```

## 3. Backend Server (server.py)

### Flask Application Structure

```python
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests for web interface
```

### Key Endpoints

#### POST /generate
Accepts JSON with parameters:
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

Returns:
```json
{
  "status": "success",
  "stl_file": "/path/to/file.stl",
  "file_size": 123456
}
```

#### GET /download/<filename>
Downloads the generated STL file

#### GET /health
Health check endpoint

### STL Generation Process

1. **Read JSCAD Template**: Load braille.jscad
2. **Append Parameters**: Override with user parameters
3. **Generate Geometry**: Create 3D model
4. **Output STL**: Generate STL file from geometry

### ASCII STL Format (Simplified)

```
solid braille_plate
  facet normal 0.0 0.0 1.0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 1.0 0.0 0.0
      vertex 0.0 1.0 0.0
    endloop
  endfacet
endsolid braille_plate
```

## 4. Web GUI (index.html)

### Technology Stack

- **THREE.js**: 3D rendering (WebGL)
- **HTML5/CSS3**: Modern UI
- **Fetch API**: Backend communication
- **Web Canvas**: 3D preview

### Key Components

#### 3D Preview Engine
```javascript
// Initialize THREE.js scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(...);
const renderer = new THREE.WebGLRenderer({canvas: ...});

// Add lighting
const light1 = new THREE.DirectionalLight(0xffffff, 0.8);
scene.add(light1);
```

#### Mouse Controls
- **Drag**: Rotate model (X, Y axes)
- **Scroll**: Zoom in/out

#### Form Communication
```javascript
fetch('/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        text: ...,
        pageSize: ...,
        // ... other parameters
    })
});
```

## 5. Data Flow

### Complete Request/Response Cycle

```
┌──────────────────────────────────────────────────────┐
│ User fills form and clicks "Generate"                │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ JavaScript: Collect form data → JSON                 │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ HTTP POST /generate (with JSON body)                 │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ Flask: Receive request                               │
│  - Parse JSON                                        │
│  - Validate inputs                                   │
│  - Load braille.jscad                                │
│  - Override parameters                               │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ JSCAD Runtime: Execute braille.jscad                 │
│  - Run main(params)                                  │
│  - Apply page size logic                             │
│  - Apply scaling                                     │
│  - Generate CSG geometry                             │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ STL Exporter: Convert to STL                         │
│  - Triangulate geometry                              │
│  - Calculate normals                                 │
│  - Write ASCII/Binary STL                            │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ HTTP Response: JSON with file path & size            │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ JavaScript: Update preview                           │
│  - Create THREE.js geometry                          │
│  - Render 3D model                                   │
│  - Display file info                                 │
│  - Enable Download button                            │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ User clicks "Download STL"                           │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ HTTP GET /download/<filename>                        │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ Flask: Send file to browser                          │
└────────────────────┬─────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────┐
│ Browser: Download file to user's Downloads folder    │
└──────────────────────────────────────────────────────┘
```

## 6. Performance Optimization Notes

### Memory Efficiency
- Temporary files cleaned up after use
- CORS enabled for efficient resource loading
- Geometry streamed directly to download

### Scaling Performance
- Scale calculation is O(1) - constant time
- No recursive operations
- Single geometric transformation

### STL File Size
```
Binary STL = 80 bytes (header) + 4 bytes (count) + 50 bytes per triangle
ASCII STL ≈ ~200 bytes per triangle (less efficient)
```

## 7. Extension Points

### To Add New Features

1. **New Page Size**:
   - Add to `pageSizes` object in braille.jscad
   - Add option to dropdown in index.html

2. **New Braille Dialect**:
   - Add to `brailleMapSingleChar` in braille.jscad
   - Create new dialect handling in jscad

3. **New Braille Style**:
   - Modify `diameter` or `spacing` in braille.jscad
   - Adjust `plate_thickness` for different back plate sizes

4. **Batch Processing**:
   - Add queue system in server.py
   - Create job tracking API

## Summary of Changes

| Component | Change | Impact |
|-----------|--------|--------|
| braille.jscad | Added pageSize parameters | Users can specify output size |
| braille.jscad | Added scaling algorithm | Content fits automatically |
| server.py | New Flask backend | No command-line needed |
| index.html | New web interface | User-friendly GUI |
| - | New startup scripts | Easy installation |

---

**Technical Implementation Complete! 🚀**
