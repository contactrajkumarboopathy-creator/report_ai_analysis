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
    Download analysis results as a file
    """
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'No content provided'}), 400
        
        filename = data.get('filename', 'analysis_result.txt')
        content = data.get('content', '')
        
        # Create file-like object
        output = io.BytesIO()
        output.write(content.encode('utf-8'))
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=True,
            download_name=f'analysis_{filename}',
            mimetype='text/plain'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'OK', 'message': 'API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
