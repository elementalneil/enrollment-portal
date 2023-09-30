from flask import Flask
from db_init import initialize

app = Flask(__name__)

initialize()

@app.route("/")
def index():
    return "<h2>Index Page</h2>"