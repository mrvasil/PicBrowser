import uuid
import os
import exiftool
import sqlite3

class Database:
    @staticmethod
    def get_connection():
        conn = sqlite3.connect('uploads/database.db')
        return conn

    @staticmethod
    def close_connection(conn):
        conn.close()

def init_db(user_code):
    conn = Database.get_connection()
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS "{user_code}" (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT NOT NULL,
                  visible BOOLEAN NOT NULL DEFAULT 1,
                  order_index INTEGER DEFAULT 0
                )''')
    conn.commit()
    Database.close_connection(conn)

def add_image_to_db(user_code, filename):
    conn = Database.get_connection()
    c = conn.cursor()

    c.execute(f'''UPDATE "{user_code}" SET visible = 1 WHERE filename = ? AND visible = 0''', (filename,))
    if c.rowcount == 0:
        c.execute(f'''INSERT INTO "{user_code}" (filename) VALUES (?)''', (filename,))
    conn.commit()
    Database.close_connection(conn)

def remove_image_from_db(user_code, filename):
    conn = Database.get_connection()
    c = conn.cursor()
    c.execute(f'''UPDATE "{user_code}" SET visible = 0 WHERE filename = ?''', (filename,))
    conn.commit()
    Database.close_connection(conn)

def get_visible_images(user_code):
    conn = Database.get_connection()
    c = conn.cursor()
    c.execute(f'''SELECT filename FROM "{user_code}" WHERE visible = 1 ORDER BY order_index, id''')
    images = [row[0] for row in c.fetchall()]
    Database.close_connection(conn)
    return images

def update_image_order(user_code, filename, new_index):
    conn = Database.get_connection()
    c = conn.cursor()

    c.execute(f'''SELECT filename, order_index FROM "{user_code}" WHERE visible = 1 ORDER BY order_index, id''')
    files = c.fetchall()

    updated_files = []
    for f in files:
        if f[0] == filename:
            continue
        updated_files.append(f)

    updated_files.insert(new_index, (filename, 0))

    for index, file in enumerate(updated_files):
        c.execute(f'''UPDATE "{user_code}" SET order_index = ? WHERE filename = ?''', (index, file[0]))
    conn.commit()
    Database.close_connection(conn)

def get_user_code(request):
    user_code = request.cookies.get('user_code')
    if not user_code:
        user_code = str(uuid.uuid4())
        os.makedirs(os.path.join('uploads', user_code), exist_ok=True)
        init_db(user_code)
    user_folder_path = os.path.join('uploads', user_code)
    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)
        init_db(user_code)
    return user_code

def get_metadata(image_path):
    try:
        with exiftool.ExifTool() as et:
            metadata = et.execute_json('-G', '-j', image_path)

            specific_data = {}

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