from flask import Blueprint, request, render_template, send_file
from typing import Final
import json

# Blueprint Initialization
app = Blueprint("downloads", __name__)

# Constants
DB_FILE: Final[str] = "databases/challenges.json"


@app.route("/downloads/")
def downloads():
    with open(DB_FILE, "r") as f:
        challenges: list[dict] = json.load(f)
    download_id = request.args.get(key='id', type=int)
    if download_id is None:
        return {"success": False, "error": "Specify `id` as url parameter"}, 400
    download_file = request.args.get(key='file', type=str)
    if download_file is not None:
        try:
            return send_file(f"files/{str(download_id)}/{download_file}", as_attachment=True), 200
        except FileNotFoundError:
            return {"success": False, "error": "File not found"}, 404
    for i in challenges:
        if i['id'] == download_id:
            return render_template("files.html", challenge=i, id=str(download_id)), 200
    return {"success": False, "error": "challenge with such id not found"}, 404
