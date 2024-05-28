from interface import app
from flask import render_template, send_file, request, jsonify
from werkzeug.utils import secure_filename
import os

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/main')
def page1():
    return render_template("main.html")

@app.route('/upload')
def page2():
    return render_template("upload.html")

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    if 'files[]' not in request.files:
        return "No files part", 400
    files = request.files.getlist('files[]')
    for file in files:
        if file.filename == '':
            return "No selected file", 400
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))
    return "Files successfully uploaded", 200

@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return "Zip file successfully uploaded", 200
    return "Invalid file type", 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'zip'}