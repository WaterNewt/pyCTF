from flask import Flask, request, render_template, url_for, session, redirect
import requests
import json
from dotenv import load_dotenv
from blueprints.downloads import app as downloads
from blueprints.verify import app as verify
from blueprints.account import app as account
from typing import Final
import os

load_dotenv("KEY.env")
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(downloads)
app.register_blueprint(verify)
app.register_blueprint(account)


DB_FILE: Final[str] = "databases/challenges.json"
USERS_DB_FILE: Final[str] = "databases/users.json"


@app.route("/", methods=['GET', 'POST'])
def index():
    with open(DB_FILE, 'r') as f:
        challenges = json.load(f)
    with open(USERS_DB_FILE, 'r') as f:
        users = json.load(f)
    for index,i in enumerate(users):
        try:
            if i['session'] == session['session']:
                if request.method == 'GET':
                    return render_template("index.html", challenges=challenges, user=i)
                if request.method == 'POST':
                    flag = request.form.get('flag', type=str)
                    id = request.form.get('id', type=int)
                    for i in challenges:
                        if i['id'] == id:
                            verify_url = "http://"+request.host+url_for("verify.verify")+"?id="+str(id)+"&flag="+flag
                            response = requests.get(verify_url)
                            if response.json()['success'] is True:
                                users[index]['completed'].append(int(id))
                                users[index]['points'] += challenges[id]['points']
                                with open(USERS_DB_FILE, 'w') as f:
                                    json.dump(users, f)
                                return "Flag is correct!"
                            else:
                                return "Flag is incorrect!"
        except KeyError:
            break
    return redirect(url_for("account.login"))


if __name__ == "__main__":
    app.run('0.0.0.0', 8000, True)
