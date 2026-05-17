// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const submitBtn = document.getElementById('submitBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');
const resultFileName = document.getElementById('resultFileName');
const resultModel = document.getElementById('resultModel');
const resultTime = document.getElementById('resultTime');
const analysisText = document.getElementById('analysisText');
const downloadBtn = document.getElementById('downloadBtn');
const copyBtn = document.getElementById('copyBtn');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const closeResults = document.getElementById('closeResults');
const copyFeedback = document.getElementById('copyFeedback');

// Store current analysis data
let currentAnalysis = null;

// File input change handler
fileInput.addEventListener('change', function() {
    if (this.files && this.files[0]) {
        fileName.textContent = `✓ Selected: ${this.files[0].name}`;
        errorMessage.classList.add('hidden');
    } else {
        fileName.textContent = '';
    }
});

// Form submission
uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (!fileInput.files || fileInput.files.length === 0) {
        showError('Please select a file');
        return;
    }

    // Validate file size
    const file = fileInput.files[0];
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
        showError('File size exceeds 10MB limit');
        return;
    }

    // Show loading state
    loadingSpinner.classList.remove('hidden');
    errorMessage.classList.add('hidden');
    submitBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('model', document.getElementById('modelSelect').value);

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        // Store analysis data
        currentAnalysis = {
            filename: data.filename,
            content: data.analysis,
            model: data.model_used,
            timestamp: data.timestamp
        };

        // Display results
        displayResults(data);

    } catch (error) {
        showError(error.message);
        console.error('Error:', error);
    } finally {
        loadingSpinner.classList.add('hidden');
        submitBtn.disabled = false;
    }
});

// Display results
function displayResults(data) {
    resultFileName.textContent = data.filename;
    resultModel.textContent = data.model_used || 'Gemini';
    resultTime.textContent = new Date(data.timestamp).toLocaleString();
    analysisText.textContent = data.analysis;
    
    // Scroll to results
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Download analysis results
downloadBtn.addEventListener('click', async function() {
    if (!currentAnalysis) return;

    const downloadData = {
        filename: currentAnalysis.filename,
        content: currentAnalysis.content,
        model: currentAnalysis.model,
        timestamp: currentAnalysis.timestamp
    };

    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(downloadData)
        });

        if (!response.ok) {
            throw new Error('Download failed');
        }

        // Get filename from response headers
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'analysis_result.html';
        if (contentDisposition) {
            const match = contentDisposition.match(/filename="?([^"]+)"?/);
            if (match) filename = match[1];
        }

        // Create blob and download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
        window.URL.revokeObjectURL(url);

    } catch (error) {
        showError('Download failed: ' + error.message);
        console.error('Download error:', error);
    }
});

// Copy to clipboard
copyBtn.addEventListener('click', function() {
    if (!currentAnalysis) return;

    const textToCopy = `ANALYSIS REPORT
================

File: ${currentAnalysis.filename}
Model: ${currentAnalysis.model}
Time: ${new Date(currentAnalysis.timestamp).toLocaleString()}

ANALYSIS:
${currentAnalysis.content}`;

    navigator.clipboard.writeText(textToCopy).then(() => {
        // Show feedback
        copyFeedback.classList.remove('hidden');
        setTimeout(() => {
            copyFeedback.classList.add('hidden');
        }, 2000);
    }).catch(() => {
        showError('Failed to copy to clipboard');
    });
});

// New analysis
newAnalysisBtn.addEventListener('click', function() {
    // Reset form
    uploadForm.reset();
    fileName.textContent = '';
    errorMessage.classList.add('hidden');
    resultsSection.classList.add('hidden');
    fileInput.focus();
    currentAnalysis = null;
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Close results
closeResults.addEventListener('click', function() {
    resultsSection.classList.add('hidden');
    uploadForm.reset();
    fileName.textContent = '';
    fileInput.focus();
});

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Check API health on page load
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => console.log('API Status:', data))
        .catch(error => console.warn('API health check failed:', error));
});
