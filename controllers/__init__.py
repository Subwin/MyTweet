from flask import redirect
from flask import url_for
from flask import render_template
from flask import session
from flask import Blueprint
from flask import abort

from ..models import User
from ..models import Tweet


main = Blueprint('controllers', __name__)


# 通过 session 来获取当前登录的用户
def current_user():
    # print('session, debug', session.permanent)
    username = session.get('username', '')
    u = User.query.filter_by(username=username).first()
    return u


@main.route('/')
def index():
    view = 'login_view'
    return redirect(url_for(view))


@main.route('/timeline')
def mytimeline_view():
    u = current_user()
    all_tweets = u.tweets
    all_tweets.sort(key=lambda t: t.created_time, reverse=True)
    return render_template('mytimeline.html', user=u, all_tweets=all_tweets)


@main.route('/timeline/<username>')
def other_timeline_view(username):
    user = User.query.filter_by(username=username).first_or_404()
    view_user = current_user()
    all_tweets = user.tweets
    all_tweets.sort(key=lambda t: t.created_time, reverse=True)
    return render_template('other.html', user=user, view_user=view_user, all_tweets=all_tweets)



@main.route('/tweet/update/<tweet_id>')
def tweet_update_view(tweet_id):
    one_tweet = Tweet.query.filter_by(id=tweet_id).first_or_404()
    data_u = one_tweet.user
    cur_u = current_user()
    if data_u != cur_u:
        abort(401)
    else:
        return render_template('tweet_update.html', tweet=one_tweet, user=current_user())


@main.route('/tweet/comments/<tweet_id>')
def comments_view(tweet_id):
    view_user = current_user()
    one_tweet = Tweet.query.filter_by(id=tweet_id).first()
    user = one_tweet.user
    comments = one_tweet.comments
    comments.sort(key=lambda t: t.created_time, reverse=True)
    return render_template('comments.html', user=user, view_user = view_user, one_tweet=one_tweet, comments=comments)
