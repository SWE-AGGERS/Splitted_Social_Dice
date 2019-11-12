# encoding: utf8
import datetime as dt

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reaction(db.Model):
    __tablename__ = 'reaction'

    user_id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)