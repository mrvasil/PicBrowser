from app import app
from flask import render_template, send_file, request

@app.route('/')
def index():
    return render_template("index.html")