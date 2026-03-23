# API Reference - Braille Plate Generator

## Base URL

```
http://localhost:5000
```

## Authentication

No authentication required. All endpoints are publicly accessible.

## Content-Type

All requests with JSON body must include:
```
Content-Type: application/json
```

## Response Format

All responses are JSON unless otherwise specified.

---

## Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Description**: Check if the server is running

**Request**:
```http
GET /health HTTP/1.1
Host: localhost:5000
```

**Response** (200 OK):
```json
{
  "status": "ok",
  "service": "braille-generator"
}
```

**Use Cases**:
- Load balancer health checks
- Monitoring dashboards
- Verify server is running

**cURL Example**:
```bash
curl http://127.0.0.1:5000/health
```

**PowerShell Example**:
```powershell
Invoke-WebRequest http://127.0.0.1:5000/health | ConvertFrom-Json
```

---

### 2. Generate Braille Model

**Endpoint**: `POST /generate`

**Description**: Generate a 3D braille plate model and return STL file for download

**Request**:
```http
POST /generate HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "text": "Hello World",
  "pageSize": "A5",
  "customWidth": 100,
  "customHeight": 150,
  "backPlate": true,
  "supportPlate": true
}
```

**Request Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | Yes | - | Braille text to convert (1-1000 chars) |
| `pageSize` | string | No | "Custom" | Page size: "A5", "A6", "A7", "B5", or "Custom" |
| `customWidth` | number | No | 100 | Width in mm (50-300) |
| `customHeight` | number | No | 150 | Height in mm (50-300) |
| `backPlate` | boolean | No | true | Include 2mm base plate |
| `supportPlate` | boolean | No | true | Include support structures |

**Page Sizes** (ISO 216):

| Size | Dimensions | Use Case |
|------|-----------|----------|
| A5 | 148 × 210 mm | Standard note cards |
| A6 | 105 × 148 mm | Postcards |
| A7 | 74 × 105 mm | Small labels |
| B5 | 176 × 250 mm | Large format |
| Custom | User-defined | Special purposes |

**Response** (200 OK):
```json
{
  "status": "success",
  "filename": "braille_1234567890.123.stl",
  "file_size": 456789,
  "message": "STL generated successfully"
}
```

**Response Parameters**:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "success" on success |
| `filename` | string | Name of generated STL file |
| `file_size` | number | File size in bytes |
| `message` | string | Success message |

**Error Responses**:

**400 Bad Request** - Text required:
```json
{
  "error": "Text is required"
}
```

**400 Bad Request** - Empty text:
```json
{
  "error": "Text is empty"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Failed to generate STL file"
}
```

**cURL Example**:
```bash
curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello",
    "pageSize": "A5",
    "backPlate": true,
    "supportPlate": true
  }'
```

**PowerShell Example**:
```powershell
$body = @{
    text = "Hello"
    pageSize = "A5"
    customWidth = 148
    customHeight = 210
    backPlate = $true
    supportPlate = $true
} | ConvertTo-Json

$response = Invoke-WebRequest `
  -Uri "http://127.0.0.1:5000/generate" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

$response.Content | ConvertFrom-Json
```

**Python Example**:
```python
import requests
import json

url = "http://127.0.0.1:5000/generate"
data = {
    "text": "Hello World",
    "pageSize": "A5",
    "customWidth": 148,
    "customHeight": 210,
    "backPlate": True,
    "supportPlate": True
}

response = requests.post(url, json=data)
result = response.json()

if result['status'] == 'success':
    print(f"Generated: {result['filename']}")
    print(f"Size: {result['file_size']} bytes")
else:
    print(f"Error: {result.get('error')}")
```

**JavaScript Example**:
```javascript
const data = {
    text: "Hello World",
    pageSize: "A5",
    customWidth: 148,
    customHeight: 210,
    backPlate: true,
    supportPlate: true
};

fetch('http://localhost:5000/generate', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
    if (result.status === 'success') {
        console.log(`Generated: ${result.filename}`);
        console.log(`Size: ${result.file_size} bytes`);
    } else {
        console.error(`Error: ${result.error}`);
    }
});
```

---

### 3. Download STL File

**Endpoint**: `GET /download/<filename>`

**Description**: Download previously generated STL file

**Request**:
```http
GET /download/braille_1234567890.123.stl HTTP/1.1
Host: localhost:5000
```

**Response** (200 OK):
```
[Binary STL file content]
```

**Content-Type**: `application/octet-stream`

**Headers**:
```
Content-Disposition: attachment; filename="braille-plate.stl"
```

**Error Responses**:

**404 Not Found** - File not found:
```json
{
  "error": "File not found"
}
```

**400 Bad Request** - Invalid file:
```json
{
  "error": "Invalid file"
}
```

**cURL Example**:
```bash
curl -O http://127.0.0.1:5000/download/braille_1234567890.123.stl
```

**PowerShell Example**:
```powershell
Invoke-WebRequest `
  -Uri "http://127.0.0.1:5000/download/braille_1234567890.123.stl" `
  -OutFile "my-braille-plate.stl"
```

**Python Example**:
```python
import requests

url = "http://127.0.0.1:5000/download/braille_1234567890.123.stl"
response = requests.get(url)

if response.status_code == 200:
    with open('braille-plate.stl', 'wb') as f:
        f.write(response.content)
    print("Downloaded successfully!")
else:
    print(f"Error: {response.status_code}")
```

---

### 4. Get HTML Interface

**Endpoint**: `GET /`

**Description**: Serve the web interface

**Request**:
```http
GET / HTTP/1.1
Host: localhost:5000
```

**Response** (200 OK):
```html
<!DOCTYPE html>
[HTML content...]
```

**Content-Type**: `text/html`

**Use Cases**:
- Access web interface in browser
- Verify server is running

**Browser Example**:
```
http://localhost:5000
```

---

## Complete Workflow Example

### Step 1: Generate Model

```bash
# Generate braille model
curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello World",
    "pageSize": "A5"
  }' > response.json

# Extract filename from response
filename=$(jq -r '.filename' response.json)
```

### Step 2: Download File

```bash
# Download the generated STL file
curl -O http://127.0.0.1:5000/download/$filename
```

### Step 3: Use in 3D Slicer

```bash
# Open in Cura (example)
cura braille-plate.stl
```

---

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | OK, process response |
| 400 | Bad Request | Check request format and parameters |
| 404 | Not Found | Check filename or endpoint URL |
| 405 | Method Not Allowed | Use correct HTTP method (GET/POST) |
| 415 | Unsupported Media Type | Add Content-Type: application/json |
| 500 | Server Error | Check server logs, try again |

---

## Rate Limiting

Currently **not implemented**. No rate limits apply.

Future versions may include:
- Request throttling (e.g., 100 requests/hour)
- File size limits
- Text length limits (currently ~1000 chars)

---

## Timeouts

- **Default request timeout**: 30 seconds
- **Generation timeout**: ~3 seconds typical
- **Download timeout**: 10 seconds

---

## File Management

### Temporary Files

- **Location**: System temp directory
- **Lifetime**: Deleted after download
- **Cleanup**: Automatic after 24 hours

### STL File Format

**Type**: ASCII STL (text-based)

**Structure**:
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

**File Size**: 100 KB - 2 MB (depending on text length)

---

## Encoding

### Text Encoding

- **Input**: UTF-8
- **Characters Supported**: German alphabets, digits, some punctuation
- **German Umlauts**: ä, ö, ü, ß (fully supported)

### URL Encoding

Filename in URL should be URL-encoded:

**Example**:
```
/download/braille%201234567890.123.stl
```

---

## CORS Headers

**Enabled**: Yes (for development)

**Allowed Origins**: All

**Allowed Methods**: GET, POST, OPTIONS

**Allowed Headers**: Content-Type, Authorization

---

## Monitoring & Debugging

### Health Check Loop

```bash
# Check server every 5 seconds
while true; do
  curl -s http://127.0.0.1:5000/health | jq .
  sleep 5
done
```

### Verbose Request/Response

**cURL**:
```bash
curl -v -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"text":"Test"}'
```

**PowerShell**:
```powershell
$VerbosePreference = "Continue"
Invoke-WebRequest http://127.0.0.1:5000/generate -Method Post ...
```

---

## API Testing Tools

### Postman

1. Create new POST request
2. URL: `http://127.0.0.1:5000/generate`
3. Headers: `Content-Type: application/json`
4. Body (raw):
```json
{
  "text": "Test",
  "pageSize": "A5"
}
```
5. Send

### cURL

See examples above

### Insomnia

1. Import OpenAPI (not yet available)
2. Or manually create requests

### REST Client (VS Code)

Create `requests.rest`:
```
POST http://127.0.0.1:5000/generate
Content-Type: application/json

{
  "text": "Hello World",
  "pageSize": "A5"
}
```

---

## Versioning

**Current Version**: 2.0

**API Stability**: Stable

**Deprecation Policy**: 6-month notice before removal

### Version History

- **v2.0**: Added page sizes, improved error handling
- **v1.0**: Initial release

---

## Support & Issues

### Common Issues

**Q: "Text is required" error**
- A: Make sure you include the "text" parameter in your request

**Q: File not found when downloading**
- A: Generate first, then download within a few minutes
- Files are automatically cleaned up after 24 hours

**Q: Server returns 500 error**
- A: Check server logs, restart server, verify braille.jscad exists

### Getting Help

1. Check [TESTING_GUIDE.md](TESTING_GUIDE.md) for test examples
2. Review [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) for implementation details
3. Check [SERVER_STARTUP_GUIDE.md](SERVER_STARTUP_GUIDE.md) for troubleshooting

---

## Future Enhancements

Planned for future releases:

- Batch generation endpoint
- Queue/job status endpoint
- STL caching for frequently generated sizes
- Webhook notifications
- Custom endpoint for other 3D formats (OBJ, 3MF)
- API authentication tokens

---

## License

This API is part of the Braille Plate Generator project.

See [LICENSE](LICENSE) for details.

---

**Last Updated**: March 23, 2026
**API Version**: 2.0
**Status**: Stable
