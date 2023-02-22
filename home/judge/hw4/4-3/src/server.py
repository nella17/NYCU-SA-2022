#!/usr/bin/env python3

from flask import (
    Flask, g, request, session,
    send_from_directory,
    make_response,
    render_template, redirect
)
from subprocess import check_output
from sys import argv
import json, time

app = Flask(__name__)

@app.route('/')
def index():
    p = int(check_output(['bash', '-c', "df / | grep % | awk '{ print $5 }' | tr -d '%\n'"]).decode())
    return json.dumps({
        'disk': p / 100,
        'uptime': int(time.monotonic()),
        'time': int(time.time()),
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

