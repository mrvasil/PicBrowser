import uuid
import os
import exiftool

import exiftool

def get_metadata(image_path):
    try:
        with exiftool.ExifTool() as et:
            metadata = et.execute_json('-G', '-j', image_path)
            specific_data = "\n".join([
                f"Model: {metadata[0].get('EXIF:Model', 'N/A')}",
                f"ExposureTime: {metadata[0].get('EXIF:ExposureTime', 'N/A')}",
                f"FNumber: {metadata[0].get('EXIF:FNumber', 'N/A')}",
                f"ISO: {metadata[0].get('EXIF:ISO', 'N/A')}"
            ])
    except Exception as e:
        specific_data = f"ExifTool error: {str(e)}"
    return specific_data
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'zip'}

def get_user_code(request):
    user_code = request.cookies.get('user_code')
    if not user_code:
        user_code = str(uuid.uuid4())
        os.makedirs(os.path.join('uploads', user_code))
    return user_code
