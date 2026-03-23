# Testing Guide - Braille Plate Generator

## Overview

This document provides comprehensive guidance on testing the Braille Plate Generator. The project includes unit tests for the backend server and guidelines for manual testing.

## Quick Start - Run Tests

### Prerequisites

```powershell
pip install -r requirements.txt
pip install pytest pytest-cov  # Optional, for better test output
```

### Run All Tests

**Using unittest (built-in)**:
```powershell
python -m unittest tests.test_server -v
```

**Using pytest (if installed)**:
```powershell
pytest tests/test_server.py -v
```

### Run Specific Test Class

```powershell
# Only test health endpoint
python -m unittest tests.test_server.TestHealthEndpoint -v

# Only test error handling
python -m unittest tests.test_server.TestErrorHandling -v
```

### Run Specific Test Method

```powershell
# Only test that health endpoint exists
python -m unittest tests.test_server.TestHealthEndpoint.test_health_endpoint_exists -v
```

## Test Structure

### Test File Organization

```
tests/test_server.py
├── TestServerSetup              # Basic setup tests
├── TestHealthEndpoint           # /health endpoint tests
├── TestHomeEndpoint             # / endpoint tests
├── TestGenerateEndpoint         # /generate endpoint tests
├── TestGeneratePageSizes        # Page size variations
├── TestSTLGeneration            # STL creation functions
├── TestDownloadEndpoint         # /download endpoint tests
├── TestErrorHandling            # Error scenarios
├── TestParameterValidation      # Parameter defaults and validation
├── TestJSSCADIntegration        # JSCAD file integration
└── TestResponseFormats          # Response format validation
```

## Test Coverage

### Server Setup Tests (`TestServerSetup`)

```python
✓ test_app_exists()
  Verifies Flask app is created

✓ test_base_dir_set()
  Verifies BASE_DIR path is configured
```

**Purpose**: Ensure basic application initialization

### Health Endpoint Tests (`TestHealthEndpoint`)

```python
✓ test_health_endpoint_exists()
  Status: 200 OK
  Verify: Endpoint is accessible

✓ test_health_returns_json()
  Verify: Response is valid JSON

✓ test_health_response_content()
  Verify: Response contains correct status and service name
```

**Purpose**: Test health check endpoint for monitoring

### Generate Endpoint Tests (`TestGenerateEndpoint`)

```python
✓ test_generate_requires_post()
  Status: 405 (Method Not Allowed)
  Verify: GET requests are rejected

✓ test_generate_requires_json()
  Status: 400/415
  Verify: Non-JSON requests are rejected

✓ test_generate_requires_text()
  Status: 400 (Bad Request)
  Verify: Missing text parameter returns error

✓ test_generate_with_minimal_params()
  Status: 200 (Success)
  Verify: Generation succeeds with required parameters

✓ test_generate_response_format()
  Verify: Response includes status, filename, file_size
```

**Purpose**: Test core generation endpoint

### Page Size Tests (`TestGeneratePageSizes`)

```python
✓ test_generate_a5_size()
  Verify: A5 (148×210mm) generation works

✓ test_generate_custom_size()
  Verify: Custom dimensions work

✓ test_generate_without_support_plate()
  Verify: Generation without support plate works
```

**Purpose**: Test page size variations

### STL Generation Tests (`TestSTLGeneration`)

```python
✓ test_create_stl_box_basic()
  Verify: STL box creation returns string content

✓ test_create_stl_box_content()
  Verify: STL contains proper facet definitions
  Check: 12 triangles for box (6 faces × 2 triangles)

✓ test_create_stl_box_dimensions()
  Verify: Dimensions are used in vertices

✓ test_generate_stl_from_jscad_creates_file()
  Verify: File is created on disk
  Verify: File has content
```

**Purpose**: Test STL file generation functions

### Error Handling Tests (`TestErrorHandling`)

```python
✓ test_generate_with_empty_text()
  Status: 400
  Verify: Empty text is rejected

✓ test_generate_with_whitespace_only_text()
  Status: 400
  Verify: Whitespace-only text is rejected

✓ test_generate_with_special_characters()
  Status: 200
  Verify: German umlauts (ä, ö, ü, ß) are handled
```

**Purpose**: Test error scenarios and input validation

### Parameter Validation Tests (`TestParameterValidation`)

```python
✓ test_default_page_size()
  Verify: pageSize defaults to Custom if omitted

✓ test_default_custom_dimensions()
  Verify: custom dimensions provided if not specified

✓ test_default_plates()
  Verify: plate options default to True
```

**Purpose**: Test parameter defaults

### JSCAD Integration Tests (`TestJSSCADIntegration`)

```python
✓ test_braille_jscad_file_exists()
  Verify: braille.jscad file is present

✓ test_braille_jscad_readable()
  Verify: File can be read

✓ test_braille_jscad_contains_functions()
  Verify: Contains expected function definitions
```

**Purpose**: Verify JSCAD dependencies

## Running Tests with Output

### Verbose Output (Detailed)

```powershell
python -m unittest tests.test_server -v
```

Output shows:
```
test_app_exists (tests.test_server.TestServerSetup) ... ok
test_base_dir_set (tests.test_server.TestServerSetup) ... ok
test_health_endpoint_exists (tests.test_server.TestHealthEndpoint) ... ok
...
----------------------------------------------------------------------
Ran 50 tests in 2.345s

OK
```

### Quiet Output (Summary Only)

```powershell
python -m unittest tests.test_server
```

Output shows:
```
..................................................
----------------------------------------------------------------------
Ran 50 tests in 2.345s

OK
```

### With Code Coverage (requires pytest-cov)

```powershell
pytest tests/test_server.py --cov=server --cov-report=html
```

Creates `htmlcov/index.html` with coverage report

## Manual Testing

### Test 1: Web Interface Loading

**Steps**:
1. Start server: `python server.py`
2. Open browser: `http://127.0.0.1:5000`
3. Verify interface loads

**Expected**:
- Braille Plate Generator header visible
- Form inputs visible
- 3D canvas displays
- "Ready!" message appears

**Result**: ✓ Pass / ✗ Fail

### Test 2: Generate Braille Model

**Steps**:
1. Enter text: "Hello"
2. Select size: "A5"
3. Click "Generate 3D Model"
4. Wait for preview

**Expected**:
- Preview appears in 3D canvas
- Model information displays (vertices, file size)
- Download button becomes enabled
- Success message shows "✓ Model generated successfully!"

**Result**: ✓ Pass / ✗ Fail

### Test 3: Download STL File

**Steps**:
1. Generate model (Test 2)
2. Click "Download STL"
3. Check Downloads folder

**Expected**:
- File downloads with name like `braille-plate-2026-03-23.stl`
- File size > 0
- Success message shows
- File can be opened in text editor (shows ASCII STL format)

**Result**: ✓ Pass / ✗ Fail

### Test 4: Page Size Presets

**Steps for each size**:
1. Select page size: "A5"
2. Generate model
3. Check preview

**Test each**:
- A5 (148×210mm)
- A6 (105×148mm)
- A7 (74×105mm)
- B5 (176×250mm)

**Expected**:
- All generate successfully
- Preview updates correctly
- Download works

**Result**: ✓ Pass / ✗ Fail

### Test 5: Custom Dimensions

**Steps**:
1. Select: "Custom"
2. Set width: 120
3. Set height: 180
4. Generate model
5. Download

**Expected**:
- Model generates
- Download succeeds

**Result**: ✓ Pass / ✗ Fail

### Test 6: 3D Preview Controls

**Steps**:
1. Generate model
2. Drag mouse over canvas
3. Scroll mouse wheel

**Expected**:
- Dragging rotates model
- Scrolling zooms in/out
- Model stays rendered

**Result**: ✓ Pass / ✗ Fail

### Test 7: Plate Options

**Steps**:
1. Test with both plates checked ✓✓
2. Test with back plate only ✓✗
3. Test with support plate only ✗✓
4. Test with both unchecked ✗✗

**Expected**:
- All combinations generate successfully
- Download works for each

**Result**: ✓ Pass / ✗ Fail

### Test 8: Multi-line Text

**Steps**:
1. Enter text:
   ```
   Line 1
   Line 2
   Line 3
   ```
2. Generate model
3. Download

**Expected**:
- Model generates with multiple lines
- Download succeeds
- Dimensions increase with line count

**Result**: ✓ Pass / ✗ Fail

### Test 9: Special Characters

**Steps**:
1. Enter text: "Äöü ß Test"
2. Generate model
3. Download

**Expected**:
- German umlauts handled correctly
- Model generates successfully
- Download works

**Result**: ✓ Pass / ✗ Fail

### Test 10: Error Cases

**Test 10a: Empty Text**
- Enter: ""
- Click Generate
- Expected: Error message "Please enter some text!"

**Test 10b: Only Whitespace**
- Enter: "   "
- Click Generate
- Expected: Error message

**Test 10c: Very Long Text**
- Enter: 1000 character text
- Click Generate
- Expected: Either succeeds or shows appropriate error

**Result**: ✓ Pass / ✗ Fail for each

## Performance Testing

### Test Duration

**Measure**: How long `/generate` takes

```powershell
# Manual timing
Measure-Command {
    curl -X POST http://127.0.0.1:5000/generate `
      -H "Content-Type: application/json" `
      -d '{"text":"Test",...}'
}
```

**Expected**: 1-3 seconds

### File Size

**Measure**: Size of generated STL files

```powershell
# Check file sizes
Get-Item $env:TEMP\braille_*.stl | Select-Object Length
```

**Expected Ranges**:
- Simple text (< 50 chars): 100-300 KB
- Medium text (50-200 chars): 300-800 KB
- Large text (> 200 chars): 800 KB - 2 MB

### Memory Usage

**Measure**: Memory during generation

```powershell
# Watch memory while generating
Get-Process python | Select-Object Working set
```

**Expected**: Peak < 500 MB

## Integration Testing

### Test: Backend + Frontend

```
1. Start server ✓
2. Load web interface ✓
3. Enter text ✓
4. Generate model ✓
5. View 3D preview ✓
6. Download STL ✓
7. Open in 3D software ✓
```

**Result**: ✓ Pass / ✗ Fail

### Test: 3D Printing Pipeline

```
1. Generate STL from web interface ✓
2. Open in Cura slicer ✓
3. Preview slices ✓
4. Export G-code ✓
5. Print (optional)
```

**Result**: ✓ Pass / ✗ Fail

## Continuous Integration

### Automated Test Run (CI/CD)

```bash
# Run all tests with coverage
pytest tests/test_server.py --cov=server --cov-report=xml

# Create test results
pytest tests/test_server.py --junit-xml=test-results.xml
```

## Creating New Tests

### Test Template

```python
import unittest
from server import app

class TestNewFeature(unittest.TestCase):
    """Test description"""
    
    def setUp(self):
        """Prepare for test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_something(self):
        """Test description"""
        response = self.client.get('/path')
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        """Cleanup after test"""
        pass

if __name__ == '__main__':
    unittest.main()
```

### Add Test to Suite

1. Create test class in `tests/test_server.py`
2. Add test methods (start with `test_`)
3. Run: `python -m unittest tests.test_server.TestNewFeature -v`

### Testing a New Endpoint

```python
def test_new_endpoint_works(self):
    """Test new /endpoint"""
    payload = {'param': 'value'}
    response = self.client.post(
        '/endpoint',
        data=json.dumps(payload),
        content_type='application/json'
    )
    self.assertEqual(response.status_code, 200)
```

## Test Assertions Cheat Sheet

```python
# Equality
self.assertEqual(a, b)           # a == b
self.assertNotEqual(a, b)        # a != b

# Truth
self.assertTrue(x)               # bool(x) == True
self.assertFalse(x)              # bool(x) == False

# Container
self.assertIn(a, b)              # a in b
self.assertNotIn(a, b)           # a not in b

# Types
self.assertIsInstance(a, b)      # isinstance(a, b)
self.assertIsNone(x)             # x is None
self.assertIsNotNone(x)          # x is not None

# HTTP status codes
self.assertEqual(status, 200)    # Success
self.assertEqual(status, 400)    # Bad request
self.assertEqual(status, 404)    # Not found
self.assertEqual(status, 500)    # Server error
```

## Troubleshooting Tests

### Import Error: "No module named 'server'"

**Fix**: Run from project directory:
```powershell
cd G:\GIT\braillegenerator
python -m unittest tests.test_server -v
```

### Tests Hang or Timeout

**Fix**: Add timeout:
```powershell
timeout 30 python -m unittest tests.test_server -v
```

### Port Already in Use

**Fix**: Tests run in `TESTING` mode (no actual server), but if port blocked:
```powershell
# Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Index.html Not Found in Tests

**Expected**: Tests may fail to load index.html
**Fix**: Tests validate this gracefully (404 is OK)

## Test Results Interpretation

### All Tests Pass ✓

```
Ran 50 tests in 2.3s
OK
```
**Meaning**: All functionality working correctly

### Some Tests Fail ✗

```
FAILED (failures=2, errors=1)
```
**Meaning**: Check error messages below results

**Example error**:
```
FAIL: test_health_response_content
...
AssertionError: 'ok' != 'not_ok'
```
**Action**: Debug the failing assertion

### Test Errors

```
ERROR: test_generate_endpoint
...
ImportError: No module named 'flask'
```
**Meaning**: Missing dependency
**Fix**: `pip install -r requirements.txt`

## Checklist Before Release

- [ ] All unit tests pass
- [ ] Manual testing completed (Tests 1-10)
- [ ] Performance acceptable (1-3 sec generation)
- [ ] No console errors
- [ ] Documentation updated
- [ ] Error messages clear
- [ ] File cleanup working
- [ ] Download functionality verified

## Additional Resources

- [unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Flask Testing Guide](https://flask.palletsprojects.com/testing/)
- [pytest Documentation](https://pytest.org/)
- [Code Coverage](https://coverage.readthedocs.io/)

## Contributing Tests

When adding new features:

1. Write test first (TDD approach)
2. Add to appropriate test class or create new
3. Run: `python -m unittest tests.test_server -v`
4. Update this documentation
5. Commit: "Add tests for [feature]"

---

**Last Updated**: March 23, 2026
**Test Count**: 50 tests
**Average Runtime**: 2-3 seconds
