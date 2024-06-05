from interface import app
import functions
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
    user_code = functions.get_user_code(request)
    user_folder = os.path.join('uploads', user_code)
    image_files = functions.get_visible_images(user_code)
    image_paths = [os.path.join(user_code, file) for file in image_files]

    response =  make_response(render_template("main.html", images=image_paths))
    response.set_cookie('user_code', user_code, max_age=31536000)
    return response, 200

@app.route('/upload')
def page2():
    return render_template("upload.html")


@app.route('/uploads/<user_code>/<filename>')
def uploaded_file(user_code, filename):
    return send_file(os.path.join('../uploads', user_code, filename))





@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    user_code = functions.get_user_code(request)
    response_text = ""

    if 'files[]' not in request.files:
        return "No files part", 400

    files = request.files.getlist('files[]')
    if len(files) > 500:
        return "The number of files should not exceed 500", 400

    user_folder = os.path.join('uploads', user_code)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    for file in files:
        if file.filename == '':
            response_text += "No selected file \n"
        elif not file.content_type.startswith('image/'):
            response_text += f"Only image files are allowed ({file.filename}) \n"
        elif file.content_length > 50000000:
            response_text += f"File size should not exceed 50 MB ({file.filename}) \n"
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(user_folder, filename))
            add_result = functions.add_image_to_db(user_code, filename)
            if not add_result:
                response_text += f"Duplicate image not added ({filename}) \n"

    if response_text == "":
        response_text = "Files uploaded successfully"
        message_code = 200
    else:
        message_code = 400

    response = make_response(response_text)
    response.set_cookie('user_code', user_code, max_age=31536000)
    return response, message_code






@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    user_code = functions.get_user_code(request)
    response = make_response("ZIP file uploaded successfully")

    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400
    if file.content_length > 300000000:
        return "ZIP file size should not exceed 300 MB", 400

    user_folder = os.path.join('uploads', user_code)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    if file and functions.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)

        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(user_folder)
            for root, dirs, files in os.walk(user_folder, topdown=False):
                for name in files:
                    if name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        functions.add_image_to_db(user_code, name)
                    else:
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
    user_code = functions.get_user_code(request)
    response_text = ""

    if 'files[]' not in request.files:
        return "No files part", 400

    files = request.files.getlist('files[]')
    user_folder = os.path.join('uploads', user_code)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    for file in files:
        if file.filename == '':
            response_text += "No selected file \n"
        if not file.content_type.startswith('image/'):
            response_text += f"Only image files are allowed ({file.filename}) \n"
        if file.content_length > 50000000:
            response_text += f"File size should not exceed 50 MB ({file.filename}) \n"
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(user_folder, filename))
            functions.add_image_to_db(user_code, filename)

    if response_text == "":
        response_text = "Files uploaded successfully"
        message_code = 200
    else:
        message_code = 400

    response = make_response(response_text)
    response.set_cookie('user_code', user_code, max_age=31536000)
    return response, message_code

@app.route('/delete_image/<usercode>/<filename>', methods=['DELETE'])
def delete_image(usercode, filename):
    user_code = functions.get_user_code(request)
    file_path = os.path.join('uploads', user_code, filename)
    try:
        #os.remove(file_path)
        functions.remove_image_from_db(user_code, filename)

        response = make_response(jsonify("Success"))
        response.set_cookie('user_code', user_code, max_age=31536000)
        return response, 200
    except Exception as e:
        return jsonify("Error"), 500


@app.route('/get_metadata/<user_code>/<filename>')
def metadata(user_code, filename):
    img_path = os.path.join('uploads', user_code, filename)
    metadata = functions.get_metadata(img_path)
    return metadata




@app.route('/image_number', methods=['POST'])
def update_image_position():
    data = request.get_json()
    new_index = int(data.get('number'))
    filename = data.get('filename')
    user_code = functions.get_user_code(request)

    functions.update_image_order(user_code, filename.split('/')[-1].split('\\')[-1], new_index)

    response = make_response("ok")
    response.set_cookie('user_code', user_code, max_age=31536000)
    return response, 200
