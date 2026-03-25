"""
Braille Plate Generator - Backend Server
Handles JSCAD file processing and STL generation
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import os
import json
import logging
from pathlib import Path
import subprocess
import sys
import pkgutil
import importlib.util

# Python 3.12+ compatibility shim for Flask/frameworks that call pkgutil.get_loader
if not hasattr(pkgutil, 'get_loader'):
    def get_loader(module_name):
        # __main__ is often used for direct script invocation and has no __spec__ in Python 3.12+
        if module_name in sys.modules:
            module = sys.modules[module_name]
            if hasattr(module, '__loader__') and module.__loader__ is not None:
                return module.__loader__

        spec = importlib.util.find_spec(module_name)
        if spec:
            return spec.loader

        # Flask may call get_loader for __main__, so provide fallback behavior
        if module_name == '__main__':
            return getattr(sys.modules.get('__main__'), '__loader__', None)

        return None
    pkgutil.get_loader = get_loader

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Get the directory where the script is located
BASE_DIR = Path(__file__).parent

# Verify required files exist
required_files = ['index.html', 'braille.jscad']
for req_file in required_files:
    if not (BASE_DIR / req_file).exists():
        logger.warning(f"Warning: {req_file} not found in {BASE_DIR}")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'braille-generator'})

@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate 3D braille model
    Expected JSON:
    {
        "text": "Braille text",
        "pageSize": "A5",
        "customWidth": 100,
        "customHeight": 150,
        "backPlate": true,
        "supportPlate": true
    }
    """
    try:
        data = request.json
        
        # Validate input
        if not data.get('text'):
            return jsonify({'error': 'Text is required'}), 400
        
        text = data.get('text', '')
        page_size = data.get('pageSize', 'Custom')
        custom_width = data.get('customWidth', 100)
        custom_height = data.get('customHeight', 150)
        back_plate = data.get('backPlate', True)
        support_plate = data.get('supportPlate', True)
        binder_holes = data.get('binderHoles', False)
        dot_height = data.get('dotHeight', 1.5)
        
        # Ensure dot_height is a valid float
        try:
            dot_height = float(dot_height)
            if dot_height <= 0:
                dot_height = 1.5
        except (ValueError, TypeError):
            dot_height = 1.5
        
        logger.info(f"Generate request: text={text[:20]}..., backPlate={back_plate}, dotHeight={dot_height}")
        
        # Create temporary file for JSCAD output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jscad', delete=False) as f:
            jscad_file = f.name
            # Read the base braille.jscad file
            base_jscad_path = BASE_DIR / 'braille.jscad'
            if not base_jscad_path.exists():
                return jsonify({'error': 'braille.jscad not found'}), 500
            
            with open(base_jscad_path, 'r') as base_file:
                base_content = base_file.read()
            
            # Append parameter override
            override = f"""
// Parameter overrides from web interface
const paramsOverride = {{
    text: `{text.replace(chr(34), chr(92) + chr(34))}`,
    pageSize: '{page_size}',
    customWidth: {custom_width},
    customHeight: {custom_height},
    backPlate: {str(back_plate).lower()},
    supportPlate: {str(support_plate).lower()},
    binderHoles: {str(binder_holes).lower()}
}};

// Use overridden params
const finalParams = {{ ...{{}}, ...paramsOverride }};
"""
            f.write(base_content)
            f.write(override)
        
        # Generate STL file
        stl_file = generate_stl_from_jscad(jscad_file, text, page_size, custom_width, custom_height, back_plate, support_plate, binder_holes, dot_height)
        
        if not os.path.exists(stl_file):
            return jsonify({'error': 'Failed to generate STL file'}), 500
        
        # Get file size
        file_size = os.path.getsize(stl_file)
        
        # Return just the filename to the client
        filename = os.path.basename(stl_file)
        
        # Clean up temporary jscad file
        try:
            os.unlink(jscad_file)
        except:
            pass
        
        return jsonify({
            'status': 'success',
            'filename': filename,
            'file_size': file_size,
            'message': 'STL generated successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    """Download generated STL file"""
    try:
        # Security: only allow filenames from temp directory
        # Extract just the filename to prevent directory traversal
        safe_filename = os.path.basename(filename)
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, safe_filename)
        
        # Verify the file exists and is in temp directory
        if not os.path.exists(file_path):
            app.logger.error(f"File not found: {file_path}")
            return jsonify({'error': 'File not found'}), 404
        
        if not os.path.isfile(file_path):
            app.logger.error(f"Not a file: {file_path}")
            return jsonify({'error': 'Invalid file'}), 400
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f'braille-plate.stl',
            mimetype='application/octet-stream'
        )
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def generate_stl_from_jscad(jscad_file, text, page_size, width, height, back_plate, support_plate, binder_holes, dot_height=1.5):
    """
    Generate STL file from JSCAD file
    This is a placeholder - in production, would use OpenJSCAD library
    """
    import json
    from datetime import datetime
    
    # Create a simple STL file as demonstration
    # In production, this would use actual jscad processing
    
    stl_file = os.path.join(tempfile.gettempdir(), f'braille_{datetime.now().timestamp()}.stl')
    
    # Create a simple ASCII STL file
    with open(stl_file, 'w') as f:
        f.write(f"solid braille_plate\n")
        
        if back_plate:
            # Add simple geometry (in real scenario, this would be actual braille dots)
            # Create a simple box
            f.write(create_stl_box(width * 0.9, height * 0.9, 2))
        else:
            # Generate only braille dots with rounded tops when no back plate
            f.write(create_braille_dots_stl(text, width, height, dot_height))
            
        f.write(f"endsolid braille_plate\n")
    
    return stl_file

def create_stl_box(width, height, depth):
    """Create simple STL box geometry"""
    w2, h2, d2 = width/2, height/2, depth/2
    vertices = [
        [-w2, -h2, -d2], [w2, -h2, -d2], [w2, h2, -d2], [-w2, h2, -d2],
        [-w2, -h2, d2], [w2, -h2, d2], [w2, h2, d2], [-w2, h2, d2]
    ]
    
    # Define 12 triangles for a box
    triangles = [
        # Top face
        (0, 1, 2), (0, 2, 3),
        # Bottom face
        (4, 6, 5), (4, 7, 6),
        # Front face
        (0, 5, 1), (0, 4, 5),
        # Back face
        (2, 7, 3), (2, 6, 7),
        # Left face
        (0, 3, 7), (0, 7, 4),
        # Right face
        (1, 5, 6), (1, 6, 2)
    ]
    
    stl_content = ""
    for tri in triangles:
        v1 = vertices[tri[0]]
        v2 = vertices[tri[1]]
        v3 = vertices[tri[2]]
        
        # Calculate normal
        import math
        ax, ay, az = v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2]
        bx, by, bz = v3[0]-v1[0], v3[1]-v1[1], v3[2]-v1[2]
        nx, ny, nz = ay*bz-az*by, az*bx-ax*bz, ax*by-ay*bx
        n_len = math.sqrt(nx*nx + ny*ny + nz*nz)
        if n_len > 0:
            nx, ny, nz = nx/n_len, ny/n_len, nz/n_len
        
        stl_content += f"  facet normal {nx} {ny} {nz}\n"
        stl_content += f"    outer loop\n"
        stl_content += f"      vertex {v1[0]} {v1[1]} {v1[2]}\n"
        stl_content += f"      vertex {v2[0]} {v2[1]} {v2[2]}\n"
        stl_content += f"      vertex {v3[0]} {v3[1]} {v3[2]}\n"
        stl_content += f"    endloop\n"
        stl_content += f"  endfacet\n"
    
    return stl_content

def create_braille_dots_stl(text, width, height, dot_height=1.5):
    """Create STL geometry for braille dots only (no back plate)"""
    # Braille character map (6-dot braille)
    braille_map = {
        'a': 0b100000, 'b': 0b101000, 'c': 0b110000, 'd': 0b110100, 'e': 0b100100,
        'f': 0b111000, 'g': 0b111100, 'h': 0b101100, 'i': 0b011000, 'j': 0b011100,
        'k': 0b100010, 'l': 0b101010, 'm': 0b110010, 'n': 0b110110, 'o': 0b100110,
        'p': 0b111010, 'q': 0b111110, 'r': 0b101110, 's': 0b011010, 't': 0b011110,
        'u': 0b100011, 'v': 0b101011, 'w': 0b011101, 'x': 0b110011, 'y': 0b110111,
        'z': 0b100111, ' ': 0b000000,
        # Numbers (using number sign + letter)
        '1': 0b100000, '2': 0b101000, '3': 0b110000, '4': 0b110100, '5': 0b100100,
        '6': 0b111000, '7': 0b111100, '8': 0b101100, '9': 0b011000, '0': 0b011100,
        # German umlauts
        'ä': 0b110011, 'ö': 0b110111, 'ü': 0b100111, 'ß': 0b011101
    }
    
    dot_radius = 0.5
    dot_spacing = 2.5
    char_spacing = 6.0
    line_spacing = 10.0
    
    stl_content = ""
    current_x = 10  # Start with some margin
    current_y = 10
    max_x = 0
    max_y = 0
    
    lines = text.lower().split('\n')
    for line_index, line in enumerate(lines):
        current_x = 10
        for char_index, char in enumerate(line):
            pattern = braille_map.get(char, braille_map[' '])
            
            for dot_index in range(6):
                if pattern & (1 << dot_index):
                    dot_x = current_x + (dot_index % 2) * dot_spacing
                    dot_y = current_y + (dot_index // 2) * dot_spacing
                    
                    # Create cylinder with dome top for each dot
                    stl_content += create_stl_dome_dot(dot_x, dot_y, dot_radius, dot_height)
            
            current_x += char_spacing
        
        max_x = max(max_x, current_x)
        current_y += line_spacing
    
    max_y = current_y
    return stl_content

def create_stl_cylinder(x, y, z, radius, height):
    """Create STL geometry for a cylinder at position (x,y,z)"""
    import math
    
    segments = 8  # Number of segments for cylinder
    stl_content = ""
    
    # Create top and bottom circles
    for i in range(segments):
        angle1 = (i / segments) * 2 * math.pi
        angle2 = ((i + 1) / segments) * 2 * math.pi
        
        x1 = x + radius * math.cos(angle1)
        y1 = y + radius * math.sin(angle1)
        x2 = x + radius * math.cos(angle2)
        y2 = y + radius * math.sin(angle2)
        
        # Top face triangle
        stl_content += f"  facet normal 0 0 1\n"
        stl_content += f"    outer loop\n"
        stl_content += f"      vertex {x} {y} {z + height/2}\n"
        stl_content += f"      vertex {x1} {y1} {z + height/2}\n"
        stl_content += f"      vertex {x2} {y2} {z + height/2}\n"
        stl_content += f"    endloop\n"
        stl_content += f"  endfacet\n"
        
        # Bottom face triangle
        stl_content += f"  facet normal 0 0 -1\n"
        stl_content += f"    outer loop\n"
        stl_content += f"      vertex {x} {y} {z - height/2}\n"
        stl_content += f"      vertex {x2} {y2} {z - height/2}\n"
        stl_content += f"      vertex {x1} {y1} {z - height/2}\n"
        stl_content += f"    endloop\n"
        stl_content += f"  endfacet\n"
        
        # Side face
        x1_bottom = x1
        y1_bottom = y1
        x2_bottom = x2
        y2_bottom = y2
        
        # Calculate normal for side face
        nx = math.cos((angle1 + angle2) / 2)
        ny = math.sin((angle1 + angle2) / 2)
        
        stl_content += f"  facet normal {nx} {ny} 0\n"
        stl_content += f"    outer loop\n"
        stl_content += f"      vertex {x1} {y1} {z + height/2}\n"
        stl_content += f"      vertex {x1_bottom} {y1_bottom} {z - height/2}\n"
        stl_content += f"      vertex {x2_bottom} {y2_bottom} {z - height/2}\n"
        stl_content += f"    endloop\n"
        stl_content += f"  endfacet\n"
        
        stl_content += f"  facet normal {nx} {ny} 0\n"
        stl_content += f"    outer loop\n"
        stl_content += f"      vertex {x1} {y1} {z + height/2}\n"
        stl_content += f"      vertex {x2_bottom} {y2_bottom} {z - height/2}\n"
        stl_content += f"      vertex {x2} {y2} {z + height/2}\n"
        stl_content += f"    endloop\n"
        stl_content += f"  endfacet\n"
    
    return stl_content

def create_stl_dome_dot(x, y, radius, height):
    """Create STL geometry for a braille dot with rounded dome top"""
    import math
    
    # Ensure height is a positive value
    if height <= 0:
        height = 1.5
    
    # Create cylinder bottom + hemisphere top
    segments = 16  # Higher resolution for smoother dome
    stl_content = ""
    
    # Create base cylinder (bottom circle)
    for i in range(segments):
        angle1 = (i / segments) * 2 * math.pi
        angle2 = ((i + 1) / segments) * 2 * math.pi
        
        x1 = x + radius * math.cos(angle1)
        y1 = y + radius * math.sin(angle1)
        x2 = x + radius * math.cos(angle2)
        y2 = y + radius * math.sin(angle2)
        
        # Bottom circle triangle
        stl_content += f"  facet normal 0 0 -1\n"
        stl_content += f"    outer loop\n"
        stl_content += f"      vertex {x} {y} 0\n"
        stl_content += f"      vertex {x2} {y2} 0\n"
        stl_content += f"      vertex {x1} {y1} 0\n"
        stl_content += f"    endloop\n"
        stl_content += f"  endfacet\n"
        
        # Side face of cylinder
        nx = math.cos((angle1 + angle2) / 2)
        ny = math.sin((angle1 + angle2) / 2)
        
        stl_content += f"  facet normal {nx} {ny} 0\n"
        stl_content += f"    outer loop\n"
        stl_content += f"      vertex {x1} {y1} 0\n"
        stl_content += f"      vertex {x2} {y2} 0\n"
        stl_content += f"      vertex {x2} {y2} {height}\n"
        stl_content += f"    endloop\n"
        stl_content += f"  endfacet\n"
        
        stl_content += f"  facet normal {nx} {ny} 0\n"
        stl_content += f"    outer loop\n"
        stl_content += f"      vertex {x1} {y1} 0\n"
        stl_content += f"      vertex {x2} {y2} {height}\n"
        stl_content += f"      vertex {x1} {y1} {height}\n"
        stl_content += f"    endloop\n"
        stl_content += f"  endfacet\n"
    
    # Create hemisphere dome on top
    # Use vertical segments for hemisphere
    for v in range(segments // 2):
        # Angle along the vertical meridian of the hemisphere
        v1_angle = (v / (segments // 2)) * (math.pi / 2)
        v2_angle = ((v + 1) / (segments // 2)) * (math.pi / 2)
        
        # Radius at each level (horizontal cross-section)
        r1 = radius * math.cos(v1_angle)
        r2 = radius * math.cos(v2_angle)
        
        # Height at each level (vertical position)
        z1 = height + radius * math.sin(v1_angle)
        z2 = height + radius * math.sin(v2_angle)
        
        # Create the horizontal segments around the dome
        for h in range(segments):
            h1_angle = (h / segments) * 2 * math.pi
            h2_angle = ((h + 1) / segments) * 2 * math.pi
            
            # First ring of points (at v1_angle)
            x1_1 = x + r1 * math.cos(h1_angle)
            y1_1 = y + r1 * math.sin(h1_angle)
            x1_2 = x + r1 * math.cos(h2_angle)
            y1_2 = y + r1 * math.sin(h2_angle)
            
            # Second ring of points (at v2_angle)
            x2_1 = x + r2 * math.cos(h1_angle)
            y2_1 = y + r2 * math.sin(h1_angle)
            x2_2 = x + r2 * math.cos(h2_angle)
            y2_2 = y + r2 * math.sin(h2_angle)
            
            # Calculate surface normals (pointing outward from hemisphere)
            # For a sphere, the normal at a point is the vector from center to that point
            mid_h_angle = (h1_angle + h2_angle) / 2
            mid_v_angle = (v1_angle + v2_angle) / 2
            
            nx = math.cos(mid_v_angle) * math.cos(mid_h_angle)
            ny = math.cos(mid_v_angle) * math.sin(mid_h_angle)
            nz = math.sin(mid_v_angle)
            
            # First triangle
            stl_content += f"  facet normal {nx} {ny} {nz}\n"
            stl_content += f"    outer loop\n"
            stl_content += f"      vertex {x1_1} {y1_1} {z1}\n"
            stl_content += f"      vertex {x1_2} {y1_2} {z1}\n"
            stl_content += f"      vertex {x2_2} {y2_2} {z2}\n"
            stl_content += f"    endloop\n"
            stl_content += f"  endfacet\n"
            
            # Second triangle
            stl_content += f"  facet normal {nx} {ny} {nz}\n"
            stl_content += f"    outer loop\n"
            stl_content += f"      vertex {x1_1} {y1_1} {z1}\n"
            stl_content += f"      vertex {x2_2} {y2_2} {z2}\n"
            stl_content += f"      vertex {x2_1} {y2_1} {z2}\n"
            stl_content += f"    endloop\n"
            stl_content += f"  endfacet\n"
    
    return stl_content

@app.route('/', methods=['GET'])
def index():
    """Serve the HTML interface"""
    index_path = BASE_DIR / 'index.html'
    if not index_path.exists():
        logger.error(f"index.html not found at {index_path}")
        return jsonify({'error': f'index.html not found at {index_path}'}), 404
    try:
        return send_file(str(index_path), mimetype='text/html')
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        return jsonify({'error': f'Error serving HTML interface: {str(e)}'}), 500

if __name__ == '__main__':
    # Verify Flask-CORS is installed
    try:
        import flask_cors
    except ImportError:
        logger.error("Flask-CORS not installed. Run: pip install Flask-CORS")
        sys.exit(1)
    
    # Print startup information
    print("\n" + "="*60)
    print("  🎨 Braille Plate Generator - Server Starting")
    print("="*60)
    print(f"\nApplication Directory: {BASE_DIR}")
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"\nStarting Flask development server...")
    print(f"✓ Web Interface: http://127.0.0.1:5000")
    print(f"✓ Health Check: http://127.0.0.1:5000/health")
    print(f"\nPress CTRL+C to stop the server")
    print("="*60 + "\n")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        print("\nTroubleshooting:")
        print("  - Port 5000 already in use? Change line: app.run(port=5001)")
        print("  - Missing dependencies? Run: pip install -r requirements.txt")
        print("  - Python not found? Install Python 3.7+")
        sys.exit(1)
