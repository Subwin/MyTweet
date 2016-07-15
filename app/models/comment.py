from . import ReprMixin
from . import Update
from sqlalchemy import sql
from . import db
import time


class Comment(db.Model, ReprMixin, Update):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    post_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))

    def __init__(self, form):
        print('comment init', form)
        content = form.get('content', '')
        self.content = content
        self.created_time = int(time.time())

    def json(self):
        self.id
        extra = dict(
            post_user_id=self.post_user_id,
            comment_tweet_id=self.comment_tweet_id,
            type = 'comment',
        )
        d = {k:v for k,v in self.__dict__.items() if k not in self.blacklist()}
        d.update(extra)
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
        ]
        return b