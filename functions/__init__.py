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

def init_db():
    conn = Database.get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_code TEXT NOT NULL,
                      filename TEXT NOT NULL,
                      visible BOOLEAN NOT NULL DEFAULT 1,
                      order_index INTEGER DEFAULT 0,
                      UNIQUE(user_code, filename)
                    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_codes (
                    user_code TEXT PRIMARY KEY
            )''')
    conn.commit()
    Database.close_connection(conn)


def add_image_to_db(user_code, filename):
    conn = Database.get_connection()
    c = conn.cursor()

    c.execute('''INSERT INTO images (user_code, filename, visible) VALUES (?, ?, 1)
                  ON CONFLICT(user_code, filename) DO UPDATE SET visible = 1''', (user_code, filename))
    conn.commit()
    Database.close_connection(conn)

def remove_image_from_db(user_code, filename):
    conn = Database.get_connection()
    c = conn.cursor()
    c.execute('''UPDATE images SET visible = 0 WHERE user_code = ? AND filename = ?''', (user_code, filename))
    conn.commit()
    Database.close_connection(conn)

def get_visible_images(user_code):
    conn = Database.get_connection()
    c = conn.cursor()
    c.execute('''SELECT filename FROM images WHERE user_code = ? AND visible = 1 ORDER BY order_index, id''', (user_code,))
    images = [row[0] for row in c.fetchall()]
    Database.close_connection(conn)
    return images

def update_image_order(user_code, filename, new_index):
    conn = Database.get_connection()
    c = conn.cursor()

    c.execute('''SELECT filename, order_index FROM images WHERE user_code = ? AND visible = 1 ORDER BY order_index, id''', (user_code,))
    files = c.fetchall()

    updated_files = []
    for f in files:
        if f[0] == filename:
            continue
        updated_files.append(f)

    updated_files.insert(new_index, (filename, 0))

    for index, file in enumerate(updated_files):
        c.execute('''UPDATE images SET order_index = ? WHERE user_code = ? AND filename = ?''', (index, user_code, file[0]))
    conn.commit()
    Database.close_connection(conn)


def remove_all_images_from_db(user_code):
    conn = Database.get_connection()
    c = conn.cursor()
    try:
        c.execute('''DELETE FROM images WHERE user_code = ?''', (user_code,))
        conn.commit()
    finally:
        Database.close_connection(conn)


def get_user_code(request):
    user_code = request.cookies.get('user_code')
    conn = Database.get_connection()
    c = conn.cursor()
    
    if user_code:
        c.execute("SELECT 1 FROM user_codes WHERE user_code = ?", (user_code,))
        exists = c.fetchone()
    else:
        exists = False

    if not exists:
        user_code = str(uuid.uuid4())
        c.execute("INSERT INTO user_codes (user_code) VALUES (?)", (user_code,))
        os.makedirs(os.path.join('uploads', user_code), exist_ok=True)
    
    conn.commit()
    Database.close_connection(conn)
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