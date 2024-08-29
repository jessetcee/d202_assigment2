import re
from datetime import datetime

from flask import render_template
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = "results"):
    return render_template(
        "hello_there.html",
        name="name",
        date=datetime.now()
    )
