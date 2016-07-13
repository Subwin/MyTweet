from .reprmixin import ReprMixin
from .update import Update
from sqlalchemy import sql
from . import db


class Comment(db.Model, ReprMixin, Update):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.DateTime(timezone=True), default=sql.func.now())
    post_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))

    def __init__(self, form):
        super(Comment, self).__init__()
        self.content = form['content']

    def json(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
            'post_user_id': self.post_user_id,
            'comment_tweet_id': self.comment_tweet_id,
        }