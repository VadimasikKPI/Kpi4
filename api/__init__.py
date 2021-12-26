from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://eqsgdyhv:q6QrOywgcP3pWvzkPeQokQpqDgd7dYJI@abul.db.elephantsql.com/eqsgdyhv"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'My First API !!'