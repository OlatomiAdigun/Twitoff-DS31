"""SQLAlchemy User and Tweet models for out database"""
from flask_sqlalchemy import SQLAlchemy

# creates a DB Object from SQLAlchemy class
db = SQLAlchemy()


# Making a User table using SQLAlchemy
class User(db.Model):
    """Creates a User Table with SQlAlchemy"""
    # id column
    id = db.Column(db.BigInteger, primary_key=True)
    # name column
    name = db.Column(db.String, nullable=False)
    # keeps track of id for the newest tweet said by user
    newest_tweet_id = db.Column(db.BigInteger)

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(db.Model):
    """Keeps track of Tweets for each user"""
    id = db.Column(db.BigInteger, primary_key=True)
    tweet = db.Column(db.Unicode(300))  # allows for text and links
    tweet_vect = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey(
        'user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)


CREATE_USER_TABLE_SQL = """
  CREATE TABLE IF NOT EXIST user (
    id INT PRIMARY,
    name STRING NOT NULL
  );
"""
