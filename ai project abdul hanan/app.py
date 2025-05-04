from flask import Flask, request, render_template
import os
from resume_parser import parse_resume
from job_matcher import match_resume_to_job

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    job_desc = request.form['job_description']
    uploaded_files = request.files.getlist("resumes")
    results = []

    for file in uploaded_files:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        parsed = parse_resume(filepath)
        score = match_resume_to_job(parsed["text"], job_desc)
        parsed["match_score"] = score
        parsed["filename"] = file.filename
        results.append(parsed)

    results = sorted(results, key=lambda x: x["match_score"], reverse=True)
    return render_template('results.html', results=results, job_desc=job_desc)

if __name__ == '__main__':
    app.run(debug=True)