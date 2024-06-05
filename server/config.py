from os import environ

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt

load_dotenv(".env")

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../client/build",
    template_folder="../client/build",
)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = environ.get("SESSION_SECRET")
flask_bcrypt = Bcrypt(app)
