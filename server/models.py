# 📚 Review With Students:
# Review models
# Review MVC
# SQLAlchemy import
from flask_sqlalchemy import SQLAlchemy
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
    title = db.Column(db.String)
    genre = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    cast_members = db.relationship(
        "CastMember", back_populates="production", cascade="all, delete-orphan"
    )

    serialize_rules = ("-created_at", "-updated_at", "-cast_members.production")


class CastMember(db.Model, SerializerMixin):
    __tablename__ = "cast_members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    production_id = db.Column(
        db.Integer, db.ForeignKey("productions.id"), nullable=False
    )

    production = db.relationship("Production", back_populates="cast_members")

    serialize_rules = ("-production.cast_members",)
