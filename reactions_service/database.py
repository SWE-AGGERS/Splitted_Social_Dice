# encoding: utf8
import datetime as dt
import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Reaction(db.Model):
    __tablename__ = 'reaction'

    user_id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)

    def to_json(self):
        react_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return json.dumps(react_dict)


class Counters(db.Model):
    __tablename__ = 'counters'

    story_id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)

    def to_json(self):
        counters_d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return json.dumps(counters_d)

