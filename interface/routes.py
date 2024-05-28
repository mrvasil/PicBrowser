from interface import app
from functions import allowed_file, get_user_code
from flask import render_template, send_file, request, jsonify, make_response
from werkzeug.utils import secure_filename
import zipfile
import os
import uuid

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
    user_code = get_user_code(request)
    response = make_response("Files uploaded successfully")

    if 'files[]' not in request.files:
        return "No files part", 400

    files = request.files.getlist('files[]')
    user_folder = os.path.join('uploads', user_code)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    for file in files:
        if file.filename == '':
            return "No selected file", 400
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(user_folder, filename))

    response.set_cookie('user_code', user_code, max_age=31536000)
    return response, 200


@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    user_code = get_user_code(request)
    response = make_response("ZIP file uploaded successfully")

    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    user_folder = os.path.join('uploads', user_code)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)

        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(user_folder)
        except zipfile.BadZipFile:
            return "Failed to unzip file", 400

        os.remove(file_path)
        response.set_cookie('user_code', user_code, max_age=31536000)
        return response, 200

    return "Invalid file type", 400

@app.route('/upload_file', methods=['POST'])
def upload_file():
    user_code = get_user_code(request)
    response = make_response("Files uploaded successfully")

    if 'files[]' not in request.files:
        return "No files part", 400

    files = request.files.getlist('files[]')
    user_folder = os.path.join('uploads', user_code)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    for file in files:
        if file.filename == '':
            return "No selected file", 400
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(user_folder, filename))

    response.set_cookie('user_code', user_code, max_age=31536000)
    return response, 200