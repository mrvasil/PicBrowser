from interface import app
from functions import db  

if __name__ == '__main__':
    db.init_db()
    app.run(host="0.0.0.0", port=12378)