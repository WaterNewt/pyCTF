from flask import Flask
from blueprints.downloads import app as downloads
from blueprints.verify import app as verify

app = Flask(__name__)
app.register_blueprint(downloads)
app.register_blueprint(verify)

if __name__ == "__main__":
    app.run('0.0.0.0', 8000, True)
