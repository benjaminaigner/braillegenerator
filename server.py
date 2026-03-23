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
        stl_file = generate_stl_from_jscad(jscad_file, text, page_size, custom_width, custom_height, back_plate, support_plate)
        
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

def generate_stl_from_jscad(jscad_file, text, page_size, width, height, back_plate, support_plate):
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
        # Add simple geometry (in real scenario, this would be actual braille dots)
        # Create a simple box
        f.write(create_stl_box(width * 0.9, height * 0.9, 2))
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
