from colour import colour
import os

from flask import Flask, render_template, make_response
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def docker_debug():
    with open(os.environ.get("WWW_DATA", "helloworld.txt")) as f:
        data = f.read()
    response = make_response(render_template('docker_debug.j2', colour=colour, data=data, environs=os.environ))
    response.headers['Cache-Control'] = 'max-age=0'
    return response
