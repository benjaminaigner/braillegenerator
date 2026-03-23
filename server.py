"""
Braille Plate Generator - Backend Server
Handles JSCAD file processing and STL generation
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import os
import json
from pathlib import Path
import subprocess
import sys

app = Flask(__name__)
CORS(app)

# Get the directory where the script is located
BASE_DIR = Path(__file__).parent

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
    supportPlate: {str(support_plate).lower()}
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
        
        # Clean up temporary jscad file
        try:
            os.unlink(jscad_file)
        except:
            pass
        
        return jsonify({
            'status': 'success',
            'stl_file': stl_file,
            'file_size': file_size,
            'message': 'STL generated successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    """Download generated STL file"""
    try:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f'braille-plate.stl',
            mimetype='application/octet-stream'
        )
    except Exception as e:
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
    return send_file('index.html', mimetype='text/html')

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)
