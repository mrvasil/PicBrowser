import sqlite3
import uuid
import os

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
    c.execute('''CREATE TABLE IF NOT EXISTS user_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_code TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    resolved BOOLEAN NOT NULL DEFAULT 0
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


def log_user_action(user_code, action_type, filename):
    conn = Database.get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO user_actions (user_code, action_type, filename) VALUES (?, ?, ?)''', (user_code, action_type, filename))
    conn.commit()
    Database.close_connection(conn)

def undo_last_action(user_code):
    conn = Database.get_connection()
    c = conn.cursor()
    c.execute('''SELECT id, action_type, filename FROM user_actions WHERE user_code = ? AND resolved = 0 ORDER BY id DESC LIMIT 1''', (user_code,))
    last_action = c.fetchone()
    if last_action:
        action_id, action_type, filename = last_action
        if action_type == 'delete':
            c.execute('''UPDATE images SET visible = 1 WHERE user_code = ? AND filename = ?''', (user_code, filename))
            conn.commit()
        c.execute('''UPDATE user_actions SET resolved = 1 WHERE id = ?''', (action_id,))
        conn.commit()
    Database.close_connection(conn)

def redo_last_action(user_code):
    conn = Database.get_connection()
    c = conn.cursor()
    c.execute('''SELECT id, action_type, filename FROM user_actions WHERE user_code = ? AND resolved = 1 ORDER BY id ASC LIMIT 1''', (user_code,))
    last_resolved_action = c.fetchone()
    if last_resolved_action:
        action_id, action_type, filename = last_resolved_action
        if action_type == 'delete':
            c.execute('''UPDATE images SET visible = 0 WHERE user_code = ? AND filename = ?''', (user_code, filename))
            conn.commit()
        c.execute('''UPDATE user_actions SET resolved = 0 WHERE id = ?''', (action_id,))
        conn.commit()
    Database.close_connection(conn)