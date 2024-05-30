import uuid
import os
import exiftool

import exiftool

def get_metadata(image_path):
    try:
        with exiftool.ExifTool() as et:
            metadata = et.execute_json('-G', '-j', image_path)

            specific_data={}

            file_size_bytes = metadata[0].get('File:FileSize', '-')

            if file_size_bytes != '-':
                file_size_megabytes = int(file_size_bytes) / (1024 * 1024)
                specific_data["Размер файла"] = f"{file_size_megabytes:.1f} MB"
            else:
                specific_data["Размер файла"] = '-'

            specific_data["Тип файла"] = metadata[0].get('File:FileType', '-')
            specific_data["Разрешение"] = str(metadata[0].get('File:ImageWidth', '-')) + "x" + str(metadata[0].get('File:ImageHeight', '-'))
            specific_data["Мегапиксели"] = int(metadata[0].get('Composite:Megapixels', '-'))
            
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
