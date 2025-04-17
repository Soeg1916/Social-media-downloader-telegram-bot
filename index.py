from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bot Web Interface"

@app.route('/api')
def api_redirect():
    return redirect('/api/index')
