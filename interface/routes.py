from interface import app
from functions import allowed_file, get_user_code
from flask import render_template, send_file, request, jsonify, make_response, send_file
from werkzeug.utils import secure_filename
import zipfile
import os
import shutil

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/main')
def page1():
    user_code = get_user_code(request)
    user_folder = os.path.join('uploads', user_code)
    image_files = [f for f in os.listdir(user_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    image_paths = [os.path.join(user_code, file) for file in image_files]
    return render_template("main.html", images=image_paths)


@app.route('/upload')
def page2():
    return render_template("upload.html")


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_file(os.path.join('../uploads', filename))





@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    user_code = get_user_code(request)
    response = make_response("Files uploaded successfully")

    if 'files[]' not in request.files:
        return "No files part", 400

    files = request.files.getlist('files[]')
    if len(files) > 500:
        return "The number of files should not exceed 500", 400

    user_folder = os.path.join('uploads', user_code)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    for file in files:
        if file.filename == '' or not file.content_type.startswith('image/') or file.content_length > 50000000:
            continue
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
    if file.content_length > 300000000:  # 300 MB
        return "ZIP file size should not exceed 300 MB", 400

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
            for root, dirs, files in os.walk(user_folder, topdown=False):
                for name in files:
                    if not name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        os.remove(os.path.join(root, name))
                for name in dirs:
                    shutil.rmtree(os.path.join(root, name))
        except:
            return "Failed to unzip file", 400

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
        if not file.content_type.startswith('image/'):
            return "Only image files are allowed", 400
        if file.content_length > 50000000:
            return "File size should not exceed 50 MB", 400
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(user_folder, filename))

    response.set_cookie('user_code', user_code, max_age=31536000)
    return response, 200


@app.route('/delete_image/<usercode>/<filename>', methods=['DELETE'])
def delete_image(usercode, filename):
    user_code = get_user_code(request)
    file_path = os.path.join('uploads', user_code, filename)
    try:
        os.remove(file_path)
        return jsonify("Success"), 200
    except Exception as e:
        return jsonify("Error"), 500
    