from flask import render_template, request, redirect, url_for, jsonify
from app import app
import os

@app.route('/')
def index():
    return render_template('index.html')
