from flask import Blueprint, request
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from typing import Final
import base64
import json
import os

load_dotenv("KEY.env")
app = Blueprint("verify", __name__)

DB_FILE: Final[str] = "databases/challenges.json"


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


key = decode_data(os.getenv('KEY'))


@app.route("/verify/")
def verify():
    with open(DB_FILE, "r") as f:
        challenges = json.load(f)
    challenge_id = request.args.get(key="id", type=int)
    if challenge_id is None:
        return {"success": False, "error": "specify `id` as url arg"}, 400
    flag = request.args.get(key="flag", type=str)
    if flag is None:
        return {"success": False, "error": "specify `flag` as url arg"}, 400
    for i in challenges:
        if i['id'] == challenge_id:
            encrypted_data = decode_data(i['flag'])
            encoded_data = encode_data(encrypted_data)
            decoded_data = decode_data(encoded_data)
            decrypted_data = aes_decrypt(decoded_data, key)
            return {"success": flag == decrypted_data.decode()}, 200 if flag == decrypted_data.decode() else 401
