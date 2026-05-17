# Quick Start Guide - AI Test Report Analyzer Web UI

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables
Create a `.env` file:
```env
GEMINI_API_KEY=your_key_here
```

### Step 3: Run the Web Server
```bash
python app.py
```

### Step 4: Open in Browser
Navigate to: **http://localhost:5000**

---

## 📁 What's New?

- ✅ **app.py** - Flask web server with REST API
- ✅ **templates/index.html** - Modern web interface
- ✅ **static/style.css** - Beautiful styling
- ✅ **static/script.js** - Frontend logic & file handling
- ✅ **FRONTEND_README.md** - Detailed documentation

---

## 🎯 Using the Web Interface

1. **Upload** your test report file (TXT, LOG, JSON, CSV, MD)
2. **Select** your preferred AI model
3. **Click** "Analyze Report"
4. **Wait** for AI analysis (typically 10-30 seconds)
5. **Download** results or copy to clipboard

---

## 📊 What You Get

✓ Execution Coverage Overview  
✓ Error Root Cause Analysis  
✓ Actionable Code & Infrastructure Recommendations  
✓ Downloadable report file  

---

## 🔌 API Usage (Advanced)

### Upload and Analyze
```bash
curl -X POST \
  -F "file=@report.txt" \
  -F "model=gemini" \
  http://localhost:5000/api/analyze
```

### Download Results
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"filename":"report.txt","content":"Analysis..."}' \
  http://localhost:5000/api/download \
  --output analysis_result.txt
```

---

## ❓ FAQs

**Q: Port 5000 is busy?**  
A: Edit `app.py` and change `port=5000` to another number like `5001`

**Q: API key error?**  
A: Create `.env` file with `GEMINI_API_KEY=your_key`

**Q: File upload fails?**  
A: Check file format (.txt, .log, .json, .csv, .md) and size < 10MB

---

**For detailed documentation, see FRONTEND_README.md**
