import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from backend.main import CompetitorAnalyzer
from backend.config import PERPLEXITY_API_KEY, check_api_key

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.config['UPLOAD_FOLDER'] = 'backend/uploads'
app.config['REPORTS_FOLDER'] = 'backend/reports'

# Ensure upload and report directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/dashboard')
def dashboard():
    reports = []
    for filename in os.listdir(app.config['REPORTS_FOLDER']):
        if filename.endswith('.json'):
            with open(os.path.join(app.config['REPORTS_FOLDER'], filename), 'r') as f:
                try:
                    report_data = json.load(f)
                    reports.append({
                        'name': report_data.get('company_name', 'Unknown Company'),
                        'file': filename
                    })
                except json.JSONDecodeError:
                    # Handle empty or malformed JSON files
                    print(f"Warning: Could not decode {filename}")
    return render_template('dashboard.html', reports=reports)

@app.route('/analyze', methods=['POST'])
def analyze():
    if not check_api_key():
        return jsonify({'error': 'PERPLEXITY_API_KEY not set'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        analyzer = CompetitorAnalyzer(PERPLEXITY_API_KEY)
        
        # Determine content type and extract data
        if filename.endswith('.pdf'):
            content = analyzer.extract_pdf_content(filepath)
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

        company_name = analyzer.extract_company_name(content)
        
        try:
            results = analyzer.analyze_competitors(content, company_name)
            report_file = analyzer.save_analysis_report(results, output_file=os.path.join(app.config['REPORTS_FOLDER'], f"analysis_{company_name.replace(' ', '_')}.json"))
            return jsonify({'report_file': os.path.basename(report_file)})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/reports/<path:filename>')
def download_report(filename):
    return send_from_directory(app.config['REPORTS_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 