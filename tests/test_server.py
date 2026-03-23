"""
Unit Tests for Braille Plate Generator
Tests for server.py and core functionality
"""

import unittest
import tempfile
import os
import json
from pathlib import Path
import sys
from io import BytesIO

# Add parent directory to path for imports (go up from tests/ to root)
sys.path.insert(0, str(Path(__file__).parent.parent))

from server import app, create_stl_box, generate_stl_from_jscad, BASE_DIR


class TestServerSetup(unittest.TestCase):
    """Test basic server setup and configuration"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_app_exists(self):
        """Test that Flask app is created"""
        self.assertIsNotNone(app)
    
    def test_base_dir_set(self):
        """Test that BASE_DIR is properly configured"""
        self.assertIsNotNone(BASE_DIR)
        self.assertTrue(isinstance(BASE_DIR, Path))


class TestHealthEndpoint(unittest.TestCase):
    """Test the /health endpoint"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_endpoint_exists(self):
        """Test that /health endpoint is accessible"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
    
    def test_health_returns_json(self):
        """Test that /health returns valid JSON"""
        response = self.client.get('/health')
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
    
    def test_health_response_content(self):
        """Test that /health returns correct content"""
        response = self.client.get('/health')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['service'], 'braille-generator')


class TestHomeEndpoint(unittest.TestCase):
    """Test the / (home) endpoint"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_home_endpoint_accessible(self):
        """Test that / endpoint is accessible"""
        response = self.client.get('/')
        # Should either return 200 or 404 (if index.html doesn't exist in test)
        self.assertIn(response.status_code, [200, 404])


class TestGenerateEndpoint(unittest.TestCase):
    """Test the /generate endpoint"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_generate_requires_post(self):
        """Test that /generate requires POST method"""
        response = self.client.get('/generate')
        self.assertEqual(response.status_code, 405)  # Method not allowed
    
    def test_generate_requires_json(self):
        """Test that /generate requires JSON content"""
        response = self.client.post('/generate')
        # Should be 400 or 415 (unsupported media type)
        self.assertIn(response.status_code, [400, 415])
    
    def test_generate_requires_text(self):
        """Test that /generate requires text parameter"""
        response = self.client.post(
            '/generate',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_generate_with_minimal_params(self):
        """Test /generate with minimal required parameters"""
        payload = {
            'text': 'Test',
            'pageSize': 'A5',
            'customWidth': 100,
            'customHeight': 150,
            'backPlate': True,
            'supportPlate': True,
            'binderHoles': False
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
    
    def test_generate_response_format(self):
        """Test that /generate returns correct response format"""
        payload = {
            'text': 'Hello',
            'pageSize': 'Custom',
            'customWidth': 100,
            'customHeight': 150,
            'backPlate': True,
            'supportPlate': True,
            'binderHoles': False
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('filename', data)
        self.assertIn('file_size', data)


class TestGeneratePageSizes(unittest.TestCase):
    """Test /generate with different page sizes"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_generate_a5_size(self):
        """Test generation with A5 page size"""
        payload = {
            'text': 'A5 Test',
            'pageSize': 'A5',
            'customWidth': 100,
            'customHeight': 150,
            'backPlate': True,
            'supportPlate': False
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_generate_custom_size(self):
        """Test generation with custom page size"""
        payload = {
            'text': 'Custom Size',
            'pageSize': 'Custom',
            'customWidth': 120,
            'customHeight': 180,
            'backPlate': True,
            'supportPlate': True,
            'binderHoles': False
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_generate_without_support_plate(self):
        """Test generation without support plate"""
        payload = {
            'text': 'No Support',
            'pageSize': 'A6',
            'customWidth': 100,
            'customHeight': 150,
            'backPlate': True,
            'supportPlate': False,
            'binderHoles': False
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


class TestSTLGeneration(unittest.TestCase):
    """Test STL generation functions"""
    
    def test_create_stl_box_basic(self):
        """Test basic STL box creation"""
        stl_content = create_stl_box(100, 150, 2)
        self.assertIsInstance(stl_content, str)
        self.assertIn('facet normal', stl_content)
        self.assertIn('vertex', stl_content)
    
    def test_create_stl_box_content(self):
        """Test STL box content is valid"""
        stl_content = create_stl_box(50, 50, 1)
        # Should have 12 triangles for a box (2 per face, 6 faces)
        facet_count = stl_content.count('facet normal')
        self.assertEqual(facet_count, 12)
    
    def test_create_stl_box_dimensions(self):
        """Test that STL box respects dimensions"""
        width, height, depth = 100, 150, 2
        stl_content = create_stl_box(width, height, depth)
        
        # Check for vertices
        self.assertIn('vertex', stl_content)
        
        # Convert to float strings to verify dimensions are used
        self.assertIn('50.0', stl_content)  # half of width
        self.assertIn('75.0', stl_content)  # half of height
    
    def test_generate_stl_from_jscad_creates_file(self):
        """Test that generate_stl_from_jscad creates a file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jscad', delete=False) as f:
            f.write('// Test JSCAD file')
            test_file = f.name
        
        try:
            stl_file = generate_stl_from_jscad(
                test_file,
                'Test',
                'A5',
                100,
                150,
                True,
                True
            )
            self.assertTrue(os.path.exists(stl_file))
            self.assertTrue(os.path.getsize(stl_file) > 0)
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)
            if os.path.exists(stl_file):
                os.unlink(stl_file)


class TestDownloadEndpoint(unittest.TestCase):
    """Test the /download endpoint"""
    
    def setUp(self):
        """Set up test client and create a temporary file"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create a temporary test file
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.stl',
            delete=False,
            dir=tempfile.gettempdir()
        )
        self.temp_file.write('solid test\nendsolid test\n')
        self.temp_file.close()
        self.filename = os.path.basename(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_download_nonexistent_file(self):
        """Test downloading nonexistent file returns 404"""
        response = self.client.get('/download/nonexistent.stl')
        self.assertEqual(response.status_code, 404)
    
    def test_download_existing_file(self):
        """Test downloading existing file"""
        response = self.client.get(f'/download/{self.filename}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'solid test', response.data)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in various scenarios"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_generate_with_empty_text(self):
        """Test that empty text is rejected"""
        payload = {
            'text': '',
            'pageSize': 'A5',
            'customWidth': 100,
            'customHeight': 150,
            'backPlate': True,
            'supportPlate': True,
            'binderHoles': False
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_generate_with_whitespace_only_text(self):
        """Test that whitespace-only text is rejected"""
        payload = {
            'text': '   \n  ',
            'pageSize': 'A5',
            'customWidth': 100,
            'customHeight': 150,
            'backPlate': True,
            'supportPlate': True,
            'binderHoles': False
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_generate_with_special_characters(self):
        """Test that special characters are handled"""
        payload = {
            'text': 'ÄÖÜß äöü',
            'pageSize': 'A5',
            'customWidth': 100,
            'customHeight': 150,
            'backPlate': True,
            'supportPlate': True,
            'binderHoles': False
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


class TestParameterValidation(unittest.TestCase):
    """Test parameter validation"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_default_page_size(self):
        """Test that pageSize defaults to Custom if not provided"""
        payload = {
            'text': 'Default Size',
            'customWidth': 100,
            'customHeight': 150,
            'backPlate': True,
            'supportPlate': True,
            'binderHoles': False
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_default_custom_dimensions(self):
        """Test that custom dimensions default if not provided"""
        payload = {
            'text': 'Test',
            'pageSize': 'Custom',
            'backPlate': True,
            'supportPlate': True
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_default_plates(self):
        """Test that plate options default to True"""
        payload = {
            'text': 'Test',
            'pageSize': 'A5',
            'customWidth': 100,
            'customHeight': 150
        }
        response = self.client.post(
            '/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


class TestJSSCADIntegration(unittest.TestCase):
    """Test JSCAD file integration"""
    
    def test_braille_jscad_file_exists(self):
        """Test that braille.jscad file exists"""
        jscad_path = BASE_DIR / 'braille.jscad'
        self.assertTrue(jscad_path.exists(), f"braille.jscad not found at {jscad_path}")
    
    def test_braille_jscad_readable(self):
        """Test that braille.jscad is readable"""
        jscad_path = BASE_DIR / 'braille.jscad'
        try:
            with open(jscad_path, 'r') as f:
                content = f.read()
            self.assertGreater(len(content), 0)
        except Exception as e:
            self.fail(f"Failed to read braille.jscad: {str(e)}")
    
    def test_braille_jscad_contains_functions(self):
        """Test that braille.jscad contains expected functions"""
        jscad_path = BASE_DIR / 'braille.jscad'
        with open(jscad_path, 'r') as f:
            content = f.read()
        
        # Check for key functions
        self.assertIn('function main', content)
        self.assertIn('function getParameterDefinitions', content)
        self.assertIn('pageSize', content)


class TestResponseFormats(unittest.TestCase):
    """Test various response formats"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_json_response_format(self):
        """Test that responses are valid JSON"""
        response = self.client.get('/health')
        try:
            data = json.loads(response.data)
            self.assertIsInstance(data, dict)
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")
    
    def test_error_response_format(self):
        """Test that error responses are valid JSON"""
        response = self.client.post(
            '/generate',
            data=json.dumps({}),
            content_type='application/json'
        )
        try:
            data = json.loads(response.data)
            self.assertIsNotNone(data)
        except json.JSONDecodeError:
            self.fail("Error response is not valid JSON")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
