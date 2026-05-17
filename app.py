# Flask app to serve the frontend and handle file analysis
import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from datetime import datetime
import io

# Ensure the project root is on sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.analyzer import TestReportAnalyzer
from src.models.gemini_impl import GeminiClient

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'log', 'json', 'csv', 'md'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_file():
    """
    Handle file upload and analysis
    Returns JSON with analysis results
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], timestamp + filename)
        file.save(filepath)
        
        # Get selected model from request
        selected_model_name = request.form.get('model', 'gemini').lower()
        
        # Initialize the appropriate model
        if selected_model_name == 'gemini':
            model_client = GeminiClient()
        else:
            # Default to Gemini
            model_client = GeminiClient()
        
        # Run analysis
        analyzer = TestReportAnalyzer(model_client=model_client)
        analysis_result = analyzer.run_analysis(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'model_used': selected_model_name,
            'analysis': analysis_result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download_analysis():
    """
    Download analysis results as an HTML file
    """
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'No content provided'}), 400
        
        filename = data.get('filename', 'analysis_result.txt')
        content = data.get('content', '')
        model = data.get('model', 'Gemini')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Create HTML document
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Report - {filename}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        
        .metadata {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px 40px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .metadata-item {{
            display: flex;
            flex-direction: column;
        }}
        
        .metadata-label {{
            font-weight: 600;
            color: #667eea;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        
        .metadata-value {{
            color: #333;
            font-size: 1.1em;
            word-break: break-word;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .content h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .analysis-text {{
            white-space: pre-wrap;
            word-wrap: break-word;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            line-height: 1.8;
            color: #2c3e50;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            border-top: 2px solid #e9ecef;
        }}
        
        @media (max-width: 600px) {{
            .header {{
                padding: 25px;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .metadata {{
                grid-template-columns: 1fr;
                padding: 20px;
            }}
            
            .content {{
                padding: 20px;
            }}
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
                border-radius: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Analysis Report</h1>
            <p>AI-Generated Executive Report</p>
        </div>
        
        <div class="metadata">
            <div class="metadata-item">
                <span class="metadata-label">File Name</span>
                <span class="metadata-value">{filename}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">AI Model</span>
                <span class="metadata-value">{model}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">Generated On</span>
                <span class="metadata-value">{datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
        </div>
        
        <div class="content">
            <h2>Analysis Results</h2>
            <div class="analysis-text">{content}</div>
        </div>
        
        <div class="footer">
            <p>Generated by Report AI Analysis | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""
        
        # Create file-like object
        output = io.BytesIO()
        output.write(html_content.encode('utf-8'))
        output.seek(0)
        
        # Generate filename without extension to add .html
        base_filename = os.path.splitext(filename)[0]
        
        return send_file(
            output,
            as_attachment=True,
            download_name=f'analysis_{base_filename}.html',
            mimetype='text/html'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'OK', 'message': 'API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
