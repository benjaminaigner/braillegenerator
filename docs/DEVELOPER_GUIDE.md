# Developer Guide - Contributing to Braille Plate Generator

## Welcome Developers!

This guide will help you contribute to the Braille Plate Generator project. Whether you're fixing bugs, adding features, or improving documentation, your contributions are valued!

## Getting Started

### Prerequisites

- Python 3.7+
- Git (for version control)
- Text editor or IDE (VS Code recommended)
- Understanding of Flask, JavaScript, and JSCAD

### Development Setup

1. **Clone the repository**:
```bash
git clone https://github.com/[user]/braillegenerator.git
cd braillegenerator
```

2. **Create virtual environment** (optional but recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov  # For testing
```

4. **Verify installation**:
```bash
python server.py
```

Should show: `Running on http://127.0.0.1:5000`

---

## Project Structure

```
braillegenerator/
├── Core Files
│   ├── server.py                  # Backend server
│   ├── index.html                 # Frontend interface
│   └── braille.jscad              # 3D model definition
│
├── Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── start_server.bat           # Windows launcher
│   └── start_server.sh            # Unix launcher
│
├── docs/                          # Documentation
│   ├── README.md                  # Project overview
│   ├── INSTALLATION.md            # Setup guide
│   ├── TESTING_GUIDE.md           # Testing documentation
│   ├── CODE_ARCHITECTURE.md       # Code structure
│   ├── API_REFERENCE.md           # API documentation
│   ├── DEVELOPER_GUIDE.md         # This file
│   └── ...other docs
│
└── tests/                         # Test suite
    └── test_server.py             # Unit tests
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
git checkout -b fix/bug-description
```

Branch naming convention:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `test/` - Test improvements
- `refactor/` - Code improvements

### 2. Make Changes

Edit files as needed. Examples below.

### 3. Run Tests

```bash
python -m unittest tests.test_server -v
```

All tests must pass before committing.

### 4. Commit Changes

```bash
git add .
git commit -m "Clear, descriptive commit message"
```

Commit message format:
- Start with action verb (Add, Fix, Update, Remove)
- Be specific about what changed
- Example: "Add page size validation in generate endpoint"

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create pull request on GitHub.

---

## Adding Features

### Example 1: Add New Page Size

**Files to modify**:
1. `braille.jscad` - Add to `pageSizes`
2. `index.html` - Add to dropdown
3. `tests/test_server.py` - Add test

**Step 1: braille.jscad**

Find this section:
```javascript
const pageSizes = {
  'A5': [148, 210],
  'A6': [105, 148],
  'A7': [74, 105],
  'B5': [176, 250],
};
```

Add your page size:
```javascript
const pageSizes = {
  'A5': [148, 210],
  'A6': [105, 148],
  'A7': [74, 105],
  'B5': [176, 250],
  'Letter': [216, 279],  // Add this
};
```

**Step 2: index.html**

Find this section:
```html
<select id="pageSize">
  <option value="Custom">Custom</option>
  <option value="A5">A5 (148 x 210 mm)</option>
  <!-- ... -->
</select>
```

Add your option:
```html
<select id="pageSize">
  <option value="Custom">Custom</option>
  <option value="A5">A5 (148 x 210 mm)</option>
  <!-- ... -->
  <option value="Letter">Letter (216 x 279 mm)</option>
</select>
```

**Step 3: test_server.py**

Add test in `TestGeneratePageSizes` class:

```python
def test_generate_letter_size(self):
    """Test generation with Letter page size"""
    payload = {
        'text': 'Letter Test',
        'pageSize': 'Letter',
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
```

**Step 4: Test and commit**

```bash
python -m unittest tests.test_server -v
git add .
git commit -m "Add Letter page size (216x279mm)"
```

---

### Example 2: Add Input Validation

**File to modify**: `server.py` in `/generate` function

**Current code**:
```python
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    if not data.get('text'):
        return jsonify({'error': 'Text is required'}), 400
    text = data.get('text', '')
    # ... rest of function
```

**Add validation**:
```python
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    if not data.get('text'):
        return jsonify({'error': 'Text is required'}), 400
    
    text = data.get('text', '').strip()
    
    # NEW: Validate text length
    if len(text) == 0:
        return jsonify({'error': 'Text cannot be empty'}), 400
    if len(text) > 500:
        return jsonify({'error': 'Text too long (max 500 chars)'}), 400
    
    # NEW: Validate page dimensions
    custom_width = data.get('customWidth', 100)
    custom_height = data.get('customHeight', 150)
    
    if custom_width < 50 or custom_width > 300:
        return jsonify({'error': 'Width must be 50-300mm'}), 400
    if custom_height < 50 or custom_height > 300:
        return jsonify({'error': 'Height must be 50-300mm'}), 400
    
    # ... rest of function
```

**Add tests** in `tests/test_server.py`:

```python
def test_text_too_long(self):
    """Test that very long text is rejected"""
    payload = {
        'text': 'x' * 1000,
        'pageSize': 'A5',
        'customWidth': 100,
        'customHeight': 150,
        'backPlate': True,
        'supportPlate': True
    }
    response = self.client.post(
        '/generate',
        data=json.dumps(payload),
        content_type='application/json'
    )
    self.assertEqual(response.status_code, 400)

def test_invalid_width(self):
    """Test that invalid width is rejected"""
    payload = {
        'text': 'Test',
        'pageSize': 'Custom',
        'customWidth': 10,  # Too small
        'customHeight': 150,
        'backPlate': True,
        'supportPlate': True
    }
    response = self.client.post(
        '/generate',
        data=json.dumps(payload),
        content_type='application/json'
    )
    self.assertEqual(response.status_code, 400)
```

---

### Example 3: Improve Error Message

**File to modify**: `server.py`

**Before**:
```python
except Exception as e:
    return jsonify({'error': str(e)}), 500
```

**After**:
```python
except FileNotFoundError as e:
    logger.error(f"File not found: {str(e)}")
    return jsonify({'error': 'Required file not found. Check server setup.'}), 500
except PermissionError as e:
    logger.error(f"Permission denied: {str(e)}")
    return jsonify({'error': 'Permission denied accessing files.'}), 500
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    return jsonify({'error': 'Unknown error. Check server logs.'}), 500
```

---

## Code Style

### Python

Follow PEP 8:

```python
# Good
def generate_stl_file(text, page_size):
    """Generate STL file from text."""
    result = process(text)
    return result

# Bad
def GenerateSTL(txt,ps):
    return process(txt)


# Good - Comments explain WHY
temp_path = tempfile.mktemp()  # Cannot use delete=False on Windows
geometry.scale([scale_x, scale_y])  # Preserve aspect ratio


# Bad - Obvious comments
x = 5  # Set x to 5
```

### JavaScript

Follow conventions in `index.html`:

```javascript
// Good
function initThreeJS() {
    // Creates 3D scene for preview
    scene = new THREE.Scene();
    // ...
}

// Good - camelCase
const pageSizes = {};
const currentSTLFile = null;

// Bad - snake_case
const page_sizes = {};
const current_stl_file = null;
```

### HTML/CSS

```html
<!-- Good: Semantic HTML -->
<button class="btn-generate" id="generateBtn">Generate</button>

<!-- Good: Meaningful classes -->
<div class="form-group">
  <label for="textInput">Text:</label>
  <textarea id="textInput"></textarea>
</div>
```

---

## Testing Requirements

### Before Committing

1. **Run all tests**:
```bash
python -m unittest tests.test_server -v
```

2. **Add tests for your changes**:
```bash
# For each new feature, add at least 1 test
# For bugs, add a test that fails first, then fix it
```

3. **Check coverage**:
```bash
pytest tests/test_server.py --cov=server
```

Target: >80% code coverage

### Adding Tests

Template for new test:

```python
def test_your_feature(self):
    """Clear description of what is being tested"""
    # Arrange: Set up test data
    payload = {'param': 'value'}
    
    # Act: Perform the action
    response = self.client.post(
        '/endpoint',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    # Assert: Verify the result
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data)
    self.assertEqual(data['field'], 'expected_value')
```

---

## Documentation

### Writing Comments

```python
# Good: Comment explains WHY
# Scale geometry to fit page while maintaining aspect ratio
scale = min(scale_x, scale_y, 1.0)

# Bad: Comment states the obvious
# Create scale variable
scale = min(scale_x, scale_y, 1.0)
```

### Docstrings

```python
def generate_stl_box(width, height, depth):
    """
    Generate ASCII STL content for a rectangular box.
    
    Args:
        width (float): Box width in mm
        height (float): Box height in mm
        depth (float): Box depth in mm
    
    Returns:
        str: ASCII STL content with 12 triangles
    
    Example:
        >>> content = generate_stl_box(100, 150, 2)
        >>> 'facet normal' in content
        True
    """
```

### Update Documentation

When adding features:

1. Update relevant `.md` file
2. Add example to `API_REFERENCE.md` if it's an API change
3. Update `CODE_ARCHITECTURE.md` if structure changes
4. Add to `TESTING_GUIDE.md` manual test list

---

## Performance Considerations

### Optimize Generation

**Before**:
```python
stl_content = ""
for tri in triangles:
    stl_content += f"  facet normal..."  # String concatenation is slow
```

**After**:
```python
stl_lines = []
for tri in triangles:
    stl_lines.append(f"  facet normal...")
stl_content = "\n".join(stl_lines)  # Faster
```

### Memory Management

```python
# Good: Clean up temp files
try:
    stl_file = generate_stl(...)
    # Use file
    return stl_file
finally:
    # Cleanup happens automatically after download
```

---

## Common Issues & Solutions

### Issue: Windows paths with backslashes

```python
# Bad: Backslash escaping issues
path = 'C:\temp\file.stl'

# Good: Use Path or raw string
path = Path('C:\temp\file.stl')
path = r'C:\temp\file.stl'
```

### Issue: Port already in use

**Solution**: Edit `server.py` last line:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Changed from 5000
```

### Issue: Tests fail randomly

**Possible causes**:
- Race conditions with file creation
- Port already in use
- Missing dependencies

**Solution**:
```python
# Use unique temp directories per test
import tempfile
temp_dir = tempfile.mkdtemp()
```

---

## Pull Request Checklist

Before submitting a PR:

- [ ] Code follows project style guide
- [ ] All tests pass (`python -m unittest tests.test_server -v`)
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No unnecessary files committed
- [ ] Feature is backward compatible

---

## Useful Commands

```bash
# Run server
python server.py

# Run tests
python -m unittest tests.test_server -v

# Run specific test
python -m unittest tests.test_server.TestHealthEndpoint -v

# Check code style
pylint server.py  # If installed

# Format code
autopep8 --in-place server.py  # If installed

# Count lines of code
wc -l server.py index.html braille.jscad

# Find TODOs
grep -r "TODO\|FIXME" .

# Check git status
git status

# See changes before commit
git diff server.py
```

---

## Getting Help

### Resources

- **Code Architecture**: [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md)
- **API Reference**: [API_REFERENCE.md](API_REFERENCE.md)
- **Testing Guide**: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Flask Docs**: https://flask.palletsprojects.com/
- **JSCAD Docs**: https://en.wikibooks.org/wiki/OpenJSCAD_User_Guide
- **THREE.js Docs**: https://threejs.org/docs/

### Asking Questions

1. Check existing issues on GitHub
2. Search documentation
3. Create a GitHub issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)

---

## Code Review Guidelines

When reviewing others' code:

- ✓ Be respectful and constructive
- ✓ Check functionality works
- ✓ Verify tests pass
- ✓ Check for security issues
- ✓ Ensure code style consistency
- ✓ Look for performance issues
- ✓ Verify documentation is updated

---

## Releasing a New Version

### Version Numbering

Use semantic versioning: `MAJOR.MINOR.PATCH`

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

Example: `v2.0.3`

### Release Process

1. Update version in code/docs
2. Update CHANGELOG.md
3. Tag release: `git tag v2.0.3`
4. Create GitHub release
5. Announce on channels

---

## Additional Tips

### Debug Print Statements

```python
# Temporary debug (remove before commit)
print(f"DEBUG: value = {value}")
logger.debug(f"DEBUG: value = {value}")  # Better

# Remove with:
# grep -r "print\|DEBUG" server.py
```

### Git Tips

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# See what changed in a file
git diff server.py

# Check file history
git log -p server.py

# Find who changed a line
git blame server.py
```

---

## Questions?

- Create a GitHub issue
- Contact project maintainer
- Check documentation

---

**Last Updated**: March 23, 2026
**Version**: 2.0
**Maintained By**: Community Contributors
