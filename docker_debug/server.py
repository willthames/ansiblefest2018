import os

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def docker_debug():
    with open(os.environ.get("WWW_DATA", "helloworld.txt")) as f:
        data = f.read()
    return render_template('docker_debug.j2', data=data, environs=os.environ)
