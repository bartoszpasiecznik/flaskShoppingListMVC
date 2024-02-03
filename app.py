from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = "flash message"

CORS(app)