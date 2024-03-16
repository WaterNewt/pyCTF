from flask import Blueprint, render_template, request, session, redirect, url_for
from typing import Final
import hashlib
import secrets
import json

app = Blueprint("account", __name__)
DB_FILE: Final[str] = "databases/users.json"


def str2hash(input_string):
    input_bytes = input_string.encode('utf-8')
    blake2_hash = hashlib.blake2b(input_bytes, digest_size=32).hexdigest()
    return blake2_hash


def generate_session(k=32):
    return secrets.token_hex(k)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        with open(DB_FILE, 'r') as f:
            users = json.load(f)
        for i in users:
            try:
                if i['session'] == session['session']:
                    return redirect(url_for('index'))
            except KeyError:
                break
        return render_template("login.html")
    elif request.method == 'POST':
        with open(DB_FILE, 'r') as f:
            users: list[dict] = json.load(f)
        username = request.form.get('username')
        password = request.form.get('password')
        print(request.form)
        hashed_pass = str2hash(password)
        print(hashed_pass)
        logged_user = None
        for index, user in enumerate(users):
            if user['username'] == username:
                if user['password'] == hashed_pass:
                    logged_user = index
        if logged_user is not None:
            new_session = generate_session()
            users[index]['session'] = new_session
            with open(DB_FILE, 'w') as f:
                json.dump(users, f, indent=4)
            session['session'] = new_session
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Incorrect username or password")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
