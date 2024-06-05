# 📚 Review With Students:
# Review models
# Review MVC
# SQLAlchemy import
from config import flask_bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# 📚 Review With Students:
# What SQLAlchemy() is replacing from SQLAlchemy in phase 3

db = SQLAlchemy()
# 1. ✅ Create a Production Model
# tablename = 'Productions'
# Columns:
# title: string, genre: string, budget:float, image:string,director: string, description:string, ongoing:boolean, created_at:date time, updated_at: date time
# 2. ✅ navigate to app.py


class Production(db.Model, SerializerMixin):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    genre = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    roles = db.relationship(
        "Role", back_populates="production", cascade="all, delete-orphan"
    )

    @validates("title")
    def validate_title(self, _, title):
        if not isinstance(title, str):
            raise ValueError("Title must be a string.")
        if len(title) < 1:
            raise ValueError("Title must have at least 1 character.")
        return title

    @validates("ongoing")
    def validate_ongoing(self, _, ongoing):
        if not isinstance(ongoing, bool):
            raise ValueError("Ongoing must be a boolean.")

    cast_members = association_proxy("roles", "cast_member")

    serialize_rules = (
        "-created_at",
        "-updated_at",
        "-roles.production",
        "cast_members",
    )


class CastMember(db.Model, SerializerMixin):
    __tablename__ = "cast_members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    roles = db.relationship(
        "Role", back_populates="cast_member", cascade="all, delete-orphan"
    )

    productions = association_proxy("roles", "production")

    serialize_rules = (
        "-roles.cast_member",
        "productions",
        "-productions.roles",
        "-productions.cast_members",
        "-roles.production",
    )


class Role(db.Model, SerializerMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    production_id = db.Column(
        db.Integer, db.ForeignKey("productions.id"), nullable=False
    )
    cast_member_id = db.Column(
        db.Integer, db.ForeignKey("cast_members.id"), nullable=False
    )

    production = db.relationship("Production", back_populates="roles")
    cast_member = db.relationship("CastMember", back_populates="roles")

    serialize_rules = ("-production.roles", "-cast_member.roles")


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    serialize_rules = ("-_password_hash",)

    @hybrid_property
    def password_hash(self):
        raise Exception("Can't read password hashes")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = flask_bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def authenticate(self, password):
        return flask_bcrypt.check_password_hash(self._password_hash, password)
