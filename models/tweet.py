from .reprmixin import ReprMixin
from .update import Update
from sqlalchemy import sql
from . import db


class Tweet(db.Model, ReprMixin, Update):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.DateTime(timezone=True), default=sql.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref="tweet")

    def __init__(self, form):
        super(Tweet, self).__init__()
        self.content = form['content']

    def json(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
            'user_id': self.user_id,
        }