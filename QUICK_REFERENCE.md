# Quick Reference Card

## 🚀 Start the Server (One Command)

**Windows:**
```
start_server.bat
```

**Mac/Linux:**
```
bash start_server.sh
```

## 🌐 Access the Web GUI
```
http://localhost:5000
```

## 📝 Input Format

### Text
```
Multiple lines work with line breaks
Another line here
German umlauts: ä ö ü ß supported
```

### Page Sizes
- A5: 148 × 210 mm (standard)
- A6: 105 × 148 mm (postcard)
- A7: 74 × 105 mm (small)
- B5: 176 × 250 mm (large)
- Custom: Set your own

## ✅ Recommended Settings

| Feature | Recommended |
|---------|-------------|
| Back Plate | ✓ ON |
| Support Plates | ✓ ON |
| Page Size | A5 (for notes) |

## 📥 Export Process

1. **Enter text** → 2. **Select size** → 3. **Click Generate** → 4. **Click Download**

## 🖨️ Printing Settings

```
Printer: FDM 3D Printer
Material: PLA or PETG
Nozzle: 0.4mm
Layer Height: 0.2mm
Infill: 20%
Support: Yes (under back plate)
```

## 🔧 Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Server won't start | Check Python installed: `python --version` |
| Port in use | Edit server.py: `port=5001` |
| STL not downloading | Try different browser |
| Model looks wrong | Check page size vs text length |

## 📁 File Structure

```
braillegenerator/
├── index.html          ← Web interface
├── server.py           ← Backend (run this)
├── braille.jscad       ← 3D model definition
├── requirements.txt    ← Dependencies
├── start_server.bat    ← Windows starter
├── start_server.sh     ← Mac/Linux starter
└── README.md           ← Main docs
```

## 💡 Pro Tips

- **A5 size** = Perfect for standard note cards
- **Custom dimensions** = For special projects
- **Back plate** = Makes printing easier
- **Support plates** = Prevents warping
- **Save file date** = File name includes date for organization

## 🎯 Common Use Cases

### Make a label
1. Set: A6 size, back plate ON
2. Enter: Your text (short)
3. Download & print

### Make a note card
1. Set: A5 size, both plates ON
2. Enter: Your note (up to 3 lines)
3. Download & print

### Custom project
1. Set: Custom size
2. Enter: Your dimensions
3. Download & print

---
Last Updated: 2024
