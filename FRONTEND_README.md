# AI Test Report Analyzer - Web UI

A modern web-based interface for analyzing test reports using AI (Google Gemini or OpenAI).

## Features

✨ **Key Features:**
- 📤 **File Upload** - Upload test reports in TXT, LOG, JSON, CSV, or MD format
- 🤖 **AI Analysis** - Powered by Google Gemini and OpenAI
- 📊 **Comprehensive Insights** - Execution coverage, root cause analysis, and actionable recommendations
- 💾 **Download Results** - Save analysis as text file
- 📋 **Copy to Clipboard** - Quick copy functionality for analysis results
- 🎨 **Beautiful UI** - Modern, responsive design that works on all devices

## Project Structure

```
report_ai_analysis/
├── app.py                 # Flask web application
├── main.py               # Original CLI application
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Main web interface
├── static/
│   ├── style.css        # Styling
│   └── script.js        # Frontend logic
├── uploads/             # Uploaded files (auto-created)
├── src/
│   ├── analyzer.py      # Test report analyzer
│   └── models/
│       ├── base_client.py
│       ├── gemini_impl.py
│       └── openai_impl.py
└── reports/             # Sample reports
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or with virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# For Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# For OpenAI (optional)
OPENAI_API_KEY=your_openai_api_key_here
```

**Getting API Keys:**
- **Gemini**: Get it from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **OpenAI**: Get it from [OpenAI Platform](https://platform.openai.com/api-keys)

## Running the Application

### Start the Web Server

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Using the Web Interface

1. **Open Browser**: Navigate to `http://localhost:5000`
2. **Upload File**: Click "Choose File" and select your test report
3. **Select Model**: Choose between Google Gemini or OpenAI
4. **Analyze**: Click "Analyze Report" and wait for results
5. **Review**: Check the AI analysis with insights and recommendations
6. **Download**: Download results as a text file or copy to clipboard

## API Endpoints

### Health Check
```
GET /api/health
```
Returns API status.

### Analyze File
```
POST /api/analyze
Content-Type: multipart/form-data

Parameters:
- file: The test report file
- model: AI model to use ('gemini' or 'openai')

Response:
{
  "success": true,
  "filename": "test_report.txt",
  "model_used": "gemini",
  "analysis": "Analysis content...",
  "timestamp": "2026-05-17T10:30:00"
}
```

### Download Analysis
```
POST /api/download
Content-Type: application/json

Body:
{
  "filename": "test_report.txt",
  "content": "Analysis content..."
}

Returns: File download (analysis_filename.txt)
```

## Supported File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Text   | `.txt`    | Plain text test reports |
| Logs   | `.log`    | Application log files |
| JSON   | `.json`   | Structured test data |
| CSV    | `.csv`    | Comma-separated test results |
| Markdown | `.md`   | Markdown formatted reports |

**Max File Size**: 10 MB

## CLI Usage (Original)

You can still use the original CLI interface:

```bash
python main.py
```

This will analyze the default report at `reports/web_regression_report.txt`

## Configuration

### Upload Settings
Edit `app.py` to modify:
- `UPLOAD_FOLDER` - Where uploaded files are stored
- `ALLOWED_EXTENSIONS` - Supported file types
- `MAX_FILE_SIZE` - Maximum upload size (default: 10 MB)

### Flask Settings
```python
app.run(
    debug=True,           # Enable debug mode
    host='0.0.0.0',      # Listen on all interfaces
    port=5000            # Port number
)
```

## Troubleshooting

### Port Already in Use
If port 5000 is busy, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### API Key Issues
- Ensure `.env` file exists in project root
- Verify API keys are valid and have proper permissions
- Check rate limits on your API accounts

### File Upload Fails
- Check file format is supported (.txt, .log, .json, .csv, .md)
- Ensure file size is under 10 MB
- Clear `uploads/` folder if storage is full

### Connection Issues
- Make sure Flask server is running
- Check firewall settings
- Try accessing `http://localhost:5000` directly

## Performance Notes

- Analysis time depends on:
  - Report file size
  - AI model complexity
  - API response time
  - Network connection
- Typical analysis: 10-30 seconds
- Large files (5+ MB) may take 1-2 minutes

## Security Considerations

- Uploaded files are temporarily stored in `uploads/` folder
- Clean up old files periodically
- Use environment variables for API keys (never hardcode)
- In production, use proper HTTPS and authentication
- Implement rate limiting for public deployments

## Development

### Adding New Features

1. **Backend**: Modify `app.py` for new API endpoints
2. **Frontend**: Update `templates/index.html` and `static/script.js`
3. **Styling**: Edit `static/style.css`

### Testing

```bash
# Test API health
curl http://localhost:5000/api/health

# Test file upload (replace test.txt with your file)
curl -X POST -F "file=@test.txt" -F "model=gemini" http://localhost:5000/api/analyze
```

## License

This project is provided as-is for testing and analysis purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all API keys are correctly configured
3. Review browser console for JavaScript errors (F12)
4. Check Flask server logs for backend errors

---

**Last Updated**: May 2026  
**Version**: 2.1.1
