from interface import app
from functions import init_db

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=20191, debug=True)