from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/static/www/index.html')