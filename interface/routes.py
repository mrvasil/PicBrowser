from interface import app
from flask import render_template, send_file, request

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/main')
def page1():
    return render_template("main.html")

@app.route('/upload')
def page2():
    return render_template("upload.html")