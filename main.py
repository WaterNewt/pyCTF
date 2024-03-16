from flask import Flask, request, render_template, url_for
import requests
import json
from dotenv import load_dotenv
from blueprints.downloads import app as downloads
from blueprints.verify import app as verify
from typing import Final
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

load_dotenv("KEY.env")
app = Flask(__name__)
app.register_blueprint(downloads)
app.register_blueprint(verify)


def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    return cipher.iv + ciphertext


def aes_decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    return plaintext


def encode_data(data):
    return base64.b64encode(data).decode('utf-8')


def decode_data(encoded_data):
    data = base64.b64decode(encoded_data.encode('utf-8'))
    return data


DB_FILE: Final[str] = "databases/challenges.json"
key = decode_data(os.getenv("KEY"))


@app.route("/", methods=['GET', 'POST'])
def index():
    with open(DB_FILE, 'r') as f:
        challenges = json.load(f)
    if request.method == 'GET':
        return render_template("index.html", challenges=challenges)
    if request.method == 'POST':
        flag = request.form.get('flag', type=str)
        id = request.form.get('id', type=int)
        for i in challenges:
            if i['id'] == id:
                verify_url = "http://"+request.host+url_for("verify.verify")+"?id="+str(id)+"&flag="+flag
                response = requests.get(verify_url)
                if response.json()['success'] is True:
                    return "Flag is correct!"
                else:
                    return "Flag is incorrect!"


if __name__ == "__main__":
    app.run('0.0.0.0', 8000, True)
