"""Maps model classes to MySQL database tables for use in other modules."""

import os
from flask_sqlalchemy import SQLAlchemy
from reggie import app
from reggie.constants import global_hero_list

app.config["SQLALCHEMY_DATABASE_URI"] = ('mysql+pymysql://'
                                         + os.environ['DB_USERNAME']
                                         + ':' + os.environ['DB_PASSWORD']
                                         + '@' + os.environ['DB_URL']
                                         + '/reggiedb')
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))


# class HeroVsHero(db.Model):
#     __tablename__ = "heroVsHero"
#     index = db.Column(db.Integer, primary_key=True)
#     hero = db.Column(db.String(64))
#     for enemy_hero in global_hero_list:
#         locals()[hero] = db.Column(db.String(64))
#
#
# class PlayerOnHero(db.Model):
#     __tablename__ = "playerOnHero"
#     index = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.Integer)
#     playerID = db.Column(db.String(64))
#     for hero in global_hero_list:
#         locals()[hero] = db.Column(db.String(64))
#
#
# class NumGamesOnHero(db.Model):
#     __tablename__ = "numGamesOnHero"
#     index = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.Integer)
#     playerID = db.Column(db.String(64))
#     for hero in global_hero_list:
#         locals()[hero] = db.Column(db.String(64))
