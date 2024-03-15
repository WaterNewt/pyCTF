from flask import Flask
from blueprints.downloads import app as downloads

app = Flask(__name__)
app.register_blueprint(downloads)

if __name__ == "__main__":
    app.run('0.0.0.0', 8000, True)
