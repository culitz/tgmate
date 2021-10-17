from flask import Flask
from sqlalchemy import create_engine


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


app.run()