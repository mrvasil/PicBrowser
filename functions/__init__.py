import uuid
import os
import exiftool

def get_metadata(image_path):
    try:
        with exiftool.ExifToolHelper() as et:
            metadata = ""
            data=et.get_metadata(image_path)[0]
            for d in data:
                metadata += d+":"+str(data[d])+"\n"
    except:
        metadata = "exiftool doesn't work your device"
    return metadata

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'zip'}

def get_user_code(request):
    user_code = request.cookies.get('user_code')
    if not user_code:
        user_code = str(uuid.uuid4())
        os.makedirs(os.path.join('uploads', user_code))
    return user_code
