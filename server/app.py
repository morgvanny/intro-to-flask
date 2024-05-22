#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import CastMember, Production, db
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db, render_as_batch=True)
db.init_app(app)


@app.route("/")
def home():
    return {"something": "whatever"}


@app.route("/productions", methods=["GET", "POST"])
def productions():
    if request.method == "GET":
        productions = Production.query.all()

        return make_response(jsonify([prod.to_dict() for prod in productions]))
    if request.method == "POST":
        production_json = request.get_json()
        try:
            production = Production(
                title=production_json.get("title"),
                genre=production_json.get("genre"),
                director=production_json.get("director"),
                description=production_json.get("description"),
                budget=production_json.get("budget"),
                image=production_json.get("image"),
                ongoing=production_json.get("ongoing"),
            )

            db.session.add(production)
            try:
                db.session.commit()
            except IntegrityError:
                return make_response({"error": "Title must be unique."}, 422)

            return make_response(jsonify(production.to_dict()), 201)
        except ValueError as e:
            return make_response({"error": e.__str__()}, 422)


@app.route("/productions/<int:id>", methods=["GET", "PATCH", "DELETE"])
def production(id):
    production = Production.query.get(id)
    if not production:
        return make_response({"message": f"No production exists with id: {id}"}, 404)

    if request.method == "GET":
        return make_response(jsonify(production.to_dict()))
    if request.method == "PATCH":
        production_json = request.get_json()
        for attr in production_json:
            setattr(production, attr, production_json.get(attr))
        db.session.add(production)
        db.session.commit()
        return make_response(jsonify(production.to_dict()), 200)
    if request.method == "DELETE":
        db.session.delete(production)
        db.session.commit()
        return make_response("", 204)


class CastMembersResource(Resource):
    def get(self):
        cast_member_data = [mem.to_dict() for mem in CastMember.query.all()]
        return make_response(jsonify(cast_member_data), 200)

    def post(self):
        cast_member_json = request.get_json()
        cast_member = CastMember(name=cast_member_json.get("name"))
        db.session.add(cast_member)
        db.session.commit()

        return make_response(jsonify(cast_member.to_dict()), 201)


api.add_resource(CastMembersResource, "/cast_members")


class CastMemberResource(Resource):
    def get(self, id):
        cast_member = db.session.get(CastMember, id)
        if not cast_member:
            return make_response(
                {"message": f"No cast member exists with id: {id}"}, 404
            )
        return make_response(
            jsonify(cast_member.to_dict()),
            200,
        )

    def patch(self, id):
        cast_member = db.session.get(CastMember, id)
        if not cast_member:
            return make_response(
                {"message": f"No cast member exists with id: {id}"}, 404
            )
        cast_member_json = request.get_json()
        for attr in cast_member_json:
            setattr(cast_member, attr, cast_member_json.get(attr))
        db.session.add(cast_member)
        db.session.commit()
        return make_response(jsonify(cast_member.to_dict()), 200)

    def delete(self, id):
        cast_member = db.session.get(CastMember, id)
        if not cast_member:
            return make_response(
                {"message": f"No cast member exists with id: {id}"}, 404
            )

        db.session.delete(cast_member)
        db.session.commit()
        return make_response("", 204)


api.add_resource(CastMemberResource, "/cast_members/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)


# CRUD
#  CREATE
#  READ
#  UPDATE
#  DELETE

# ReST
#  Representational State Transfer

# CREATE - /resources - POST
# READ - /resources OR /resources/<int:id> - GET
# UPDATE - /resources/<int:id> - PATCH or PUT
# DELETE - /resources/<int:id> - DELETE
