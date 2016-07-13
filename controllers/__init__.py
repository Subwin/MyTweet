from flask import render_template
from flask import session
from flask import Blueprint

from ..models import User


main = Blueprint('controllers', __name__)


# 通过 session 来获取当前登录的用户
def current_user():
    # print('session, debug', session.permanent)
    username = session.get('username', '')
    u = User.query.filter_by(username=username).first()
    return u


@main.route('/timeline')
def mytweet_view():
    u = current_user()
    all_tweets = u.tweets
    all_tweets.sort(key=lambda t: t.created_time, reverse=True)
    return render_template('mytweet.html', user=u, all_tweets=all_tweets)


@main.route('/timeline/<username>')
def other_timeline_view(username):
    user = User.query.filter_by(username=username).first_or_404()
    view_user = current_user()
    all_tweets = user.tweets
    all_tweets.sort(key=lambda t: t.created_time, reverse=True)
    return render_template('other.html', user=user, view_user=view_user, all_tweets=all_tweets)


