from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from . import db
import uuid

class User(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4())) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_name = db.Column(db.String(1000), unique=True)
    
    @property
    def number_of_following(self):
        return Follow.query.filter_by(following=self.id).count()
    
    @property
    def number_of_followers(self):
        return Follow.query.filter_by(followers=self.id).count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'user_name': self.user_name,
            'followers': self.number_of_followers,
            'following': self.number_of_following,
        }
    
class Lyric(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user = db.Column(db.String, db.ForeignKey('user.id')) # user who uploaded lyric
    content = db.Column(db.Text)
    title = db.Column(db.String)
    # function that returns number of likes a lyric has
    @property
    def likes(self):
        return Like.query.filter_by(lyric=self.id).count()
    
    # function to change attributes of model to keys in dictionary, useful for jsonify
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'likes': self.likes,
            'title': self.title,
            'user_name': User.query.get(self.user).user_name
        }

class Review(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reviewer = db.Column(db.String, db.ForeignKey('user.id'))  # user that gave review
    lyric = db.Column(db.Integer, db.ForeignKey('lyric.id'))    # lyric that got reviewed
    review = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_name': User.query.get(self.reviewer).user_name,
            'lyric_title': Lyric.query.get(self.lyric).title,
            'review': self.review
        }

class Like(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user = db.Column(db.String, db.ForeignKey('user.id'))      # user who liked lyric
    lyric = db.Column(db.Integer, db.ForeignKey('lyric.id'))    # lyric that was liked

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': User.query.get(self.user).user_name,
            'lyric_title': Lyric.query.get(self.lyric).title,
        }

class Follow(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    follower = db.Column(db.String, db.ForeignKey('user.id'))      # follower
    following = db.Column(db.String, db.ForeignKey('user.id'))     # followee
    def to_dict(self):
        return {
            'id': self.id,
            'follower_user_name': User.query.get(self.follower).user_name,
            'following_user_name': User.query.get(self.following).user_name,
        }