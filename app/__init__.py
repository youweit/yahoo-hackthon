from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import views,models
