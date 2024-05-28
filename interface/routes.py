from interface import app
from flask import render_template, send_file, request

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/page1')
def page1():
    return render_template("page1.html")

@app.route('/page2')
def page2():
    return render_template("page2.html")