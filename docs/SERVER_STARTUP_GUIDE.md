# 🔧 Server Startup - Troubleshooting Guide

## Quick Fixes for Common Errors

### ✅ All Systems Check

Before starting the server, verify you have:

```
□ Python 3.7+ installed
□ Internet connection (for first-time set up)
□ 50 MB free disk space
□ Administrator access (optional, for installing packages)
```

### Error 1: "Python not found"

**Message**: `'python' is not recognized as an internal or external command`

**Fix**:
1. Install Python 3.7+ from https://www.python.org
2. **Important**: Check "Add Python to PATH" during installation
3. Restart your computer
4. Try again

**Verify**: Open PowerShell and run:
```powershell
python --version
```

Should show: `Python 3.x.x`

---

### Error 2: "ModuleNotFoundError: No module named 'flask'"

**Message**: `ModuleNotFoundError: No module named 'flask'`

**Fix**:
```powershell
pip install -r requirements.txt
```

Or manually:
```powershell
pip install Flask==2.3.0
pip install Flask-CORS==4.0.0
```

**Verify**:
```powershell
python -c "import flask; print(flask.__version__)"
```

Should show: `2.3.0`

---

### Error 3: "Address already in use"

**Message**: `Address already in use` or `OSError: [Errno 10048]`

**Problem**: Port 5000 is already being used

**Fix 1 - Kill existing process**:

On Windows PowerShell:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill it (replace PID with the number from above)
taskkill /PID <PID> /F
```

**Fix 2 - Use different port**:

Edit the last line of `server.py`:
```python
# Change from:
app.run(debug=True, host='127.0.0.1', port=5000)

# To:
app.run(debug=True, host='127.0.0.1', port=5001)
```

Then access: `http://localhost:5001`

---

### Error 4: "index.html not found"

**Message**: `index.html not found` or `404 Not Found`

**Problem**: `index.html` is missing or in wrong location

**Fix**:
1. Verify `index.html` exists in the same folder as `server.py`
2. Check file name is exactly `index.html` (case-sensitive on Mac/Linux)
3. Verify folder path: `G:\GIT\braillegenerator\`

**List files**:
```powershell
dir *.html
```

Should show: `index.html`

---

### Error 5: "Socket bind error"

**Message**: `socket.error: Address already in use`

**Same as Error 3** - See above

---

### Error 6: "Connection refused"

**Message**: `Error: connect ECONNREFUSED 127.0.0.1:5000`

**Problem**: Server is not running

**Fix**:
1. Start the server:
   ```powershell
   python server.py
   ```
2. Wait for message: `Running on http://127.0.0.1:5000`
3. Then open browser

---

### Error 7: "SSL: CERTIFICATE_VERIFY_FAILED"

**Message**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Problem**: SSL certificate verification issue

**Fix**:
This is usually for SSL connections. Since we're using local `http://` (not `https://`), this shouldn't occur. If it does:

```powershell
pip install --upgrade certifi
```

---

## Server Startup Checklist

### Before Running

```
Step 1: Navigate to project folder
  cd G:\GIT\braillegenerator

Step 2: Check Python
  python --version
  > Should show Python 3.7 or higher

Step 3: Install dependencies
  pip install -r requirements.txt
  > Watch for any errors

Step 4: Verify files exist
  ls *.html
  > Should include index.html
  ls braille.jscad
  > Should exist
```

### Starting Server

```
Step 5: Start server
  python server.py
  > Should see: "Running on http://127.0.0.1:5000"

Step 6: Open browser
  Go to: http://127.0.0.1:5000

Step 7: Verify it works
  - Should see web interface
  - Should see "Ready!" message
```

---

## Testing the Server

### Test 1: Is server running?
```powershell
# Open another PowerShell and run:
curl http://127.0.0.1:5000/health
```

Should return:
```json
{"status":"ok","service":"braille-generator"}
```

### Test 2: Can you load the interface?
```
Open browser: http://127.0.0.1:5000
Should see: Braille Plate Generator web interface
```

### Test 3: Is 3D preview working?
```
Enter: "Test"
Click: "Generate 3D Model"
Should see: 3D preview appear
```

### Test 4: Can you download?
```
After generating:
Click: "⬇ Download STL"
Should: Download file to Downloads folder
```

---

## Advanced Troubleshooting

### Check Python Path

```powershell
$env:Path
```

Should include Python directory (e.g., `C:\Python39\Scripts`)

### Check pip

```powershell
pip --version
```

Should show: `pip X.X.X from ...`

### Verbose server start

Add debug output:
```powershell
python -u server.py
```

The `-u` flag forces unbuffered output

### Check logs

Server writes to console. Look for:
- `WARNING` messages (non-fatal issues)
- `ERROR` messages (serious problems)

---

## Reinstall Everything

If nothing else works:

```powershell
# Step 1: Uninstall Flask
pip uninstall flask flask-cors -y

# Step 2: Clear cache
pip cache purge

# Step 3: Reinstall
pip install -r requirements.txt

# Step 4: Verify
python -c "import flask; import flask_cors; print('OK')"

# Step 5: Start
python server.py
```

---

## Getting Help

If you're still having issues:

1. **Copy the full error message**
2. **Note the exact command you ran**
3. **Check what Operating System** you're using
4. **Verify Python version**
5. **Check if firewall is blocking port 5000**

---

## Quick Diagnostic Script

Save as `diagnose.bat`:

```batch
@echo off
echo Diagnostic Report
echo =================
echo.
echo Python:
python --version
echo.
echo Pip:
pip --version
echo.
echo Flask:
python -c "import flask; print(flask.__version__)"
echo.
echo Flask-CORS:
python -c "import flask_cors; print(flask_cors.__version__)"
echo.
echo Files:
dir /b index.html
dir /b braille.jscad
dir /b server.py
echo.
echo Port 5000 usage:
netstat -ano | findstr :5000
```

Run it:
```powershell
.\diagnose.bat
```

---

## Success! 🎉

If the server starts successfully, you should see:

```
============================================================
  🎨 Braille Plate Generator - Server Starting
============================================================

Application Directory: G:\GIT\braillegenerator
Python Version: 3.9.x

Starting Flask development server...
✓ Web Interface: http://127.0.0.1:5000
✓ Health Check: http://127.0.0.1:5000/health

Press CTRL+C to stop the server
============================================================

 * Serving Flask app 'server'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Then open: **http://127.0.0.1:5000** in your browser!

---

**Still stuck?** Check the INSTALLATION.md file for more detailed setup information.