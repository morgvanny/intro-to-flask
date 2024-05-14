#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import Production, db

# 📚 Review With Students:
# Request-Response Cycle
# Web Servers and WSGI/Werkzeug

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)

# 1. ✅ Navigate to `models.py`

# 2. ✅ Set Up Imports


# 3. ✅ Initialize the App


# Configure the database
# ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'`
# ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False`


# 4. ✅ Migrate

# 5. ✅ Navigate to `seed.rb`

# 6. ✅ Routes


# 7. ✅ Run the server with `flask run` and verify your route in the browser at `http://localhost:5000/`

# 8. ✅ Create a dynamic route


# 9.✅ Update the route to find a `production` by its `title` and send it to our browser


# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below
# and run `python app.py`


@app.route("/")
def home():
    return {"something": "whatever"}


@app.route("/productions")
def productions():
    productions = Production.query.all()

    return make_response(jsonify([prod.to_dict() for prod in productions]))


@app.route("/productions/<int:id>")
def production(id):
    production = Production.query.get(id)
    if production:
        return make_response(jsonify(production.to_dict()))
    else:
        return make_response({"message": f"No production exists with id: {id}"}, 404)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
