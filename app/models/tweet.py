from . import ReprMixin
from . import Update
from sqlalchemy import sql
from . import db
import time


class Tweet(db.Model, ReprMixin, Update):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref="tweet")

    @staticmethod
    def tweet_by_id(self, tweet_id):
        return Tweet.query.filter_by(id=tweet_id).first_or_404()

    def __init__(self, form):
        print('tweet init', form)
        content = form.get('content', '')
        self.content = content
        self.created_time = int(time.time())

    def json(self):
        self.id
        extra = dict(
            user_id=self.user_id,
            type = 'tweet',
        )
        d = {k:v for k,v in self.__dict__.items() if k not in self.blacklist()}
        d.update(extra)
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
        ]
        return b