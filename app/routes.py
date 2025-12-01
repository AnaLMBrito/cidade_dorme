from app import app
from flask import render_template

@app.route('/')
#função que será renderizada
def home():
    return render_template('index.html')
