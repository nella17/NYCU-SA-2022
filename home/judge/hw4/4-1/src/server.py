#!/usr/bin/env python3

from flask import (
    Flask, g, request, session,
    send_from_directory, send_file,
    make_response,
    render_template, redirect
)
from sys import argv
import jwt
import bcrypt
import os
import base64

static_folder = os.path.join(os.getcwd(), argv[2])
argv = argv[4::2]
domain, secret, *users = argv
users = [s.split(':') for s in users]
pass_table = { username: password for username, password in users }
print(secret, users)

def encode(username):
    return jwt.encode({'user':username}, secret, algorithm='HS256')
def decode(token):
    try:
        return jwt.decode(token, secret, algorithm=['HS256'])['user']
    except:
        return None

def authenticate(username, password):
    hashed = pass_table.get(username, '').encode()
    return bcrypt.checkpw(password.encode(), hashed)

app = Flask(__name__)

def log(*x):
    pass
    #  with open('log', 'w+') as f: f.write(str(x)+'\n')

def getdata():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        return request.json
    return request.form

@app.route('/login', methods=['POST'])
def login():
    data = getdata()
    username = data.get('username', '')
    password = data.get('password', '')
    if authenticate(username, password):
        return encode(username)
    return make_response('', 403)

@app.route('/', defaults={ 'path': '' })
@app.route('/<path:path>')
def index(path):
    log(f'get {path}', request.headers)
    owner = path.split('/')[0]
    method, auth = request.headers.get('Authorization', ' ').split(' ')
    user = None
    if method == 'Basic':
        auth = base64.b64decode(auth.encode()).decode().split(':')
        if authenticate(*auth):
            user = auth[0]
    if method == 'Bearer':
        user = decode(auth)
    realpath = os.path.join(static_folder, path)
    log(realpath, static_folder, path, auth, user, owner)
    if owner == user or owner == 'public' and os.path.isfile(realpath):
        return send_from_directory(static_folder, path)
    return make_response('', 403)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
