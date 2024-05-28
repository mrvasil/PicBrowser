import uuid
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'zip'}

def get_user_code(request):
    user_code = request.cookies.get('user_code')
    if not user_code:
        user_code = str(uuid.uuid4())
        os.makedirs(os.path.join('uploads', user_code))
    return user_code
