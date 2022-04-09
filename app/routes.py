from app import app
from flask import render_template

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/2')
def display():
    return render_template('display.html')