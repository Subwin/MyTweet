from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import jsonify
from flask import session
from flask import abort
from flask_sqlalchemy import SQLAlchemy

from models import User
from models import Tweet
from models import Comment
app = Flask(__name__)
app.secret_key = 'random string'


# 通过 session 来获取当前登录的用户
def current_user():
    # print('session, debug', session.permanent)
    username = session.get('username', '')
    u = User.query.filter_by(username=username).first()
    return u


@app.route('/')
def index():
    view = 'login_view'
    return redirect(url_for(view))


# # 显示登录界面的函数  GET
# @app.route('/login')
# def login_view():
#     template = 'login.html'
#     return render_template(template)
#
#
# # 处理登录请求  POST
# @app.route('/login', methods=['POST'])
# def login():
#     form = request.get_json()
#     username = form.get('username', '')
#     user = User.query.filter_by(username=username).first()
#     r = {
#         'success': True,
#         'message': '登录成功',
#     }
#     if user is not None and user.validate_auth(form):
#         r['success'] = True
#         r['next'] = url_for('timeline', username=user.username)
#         session.permanent = True
#         session['username'] = username
#     else:
#         r['success'] = False
#         r['message'] = '登录失败'
#     return jsonify(r)
#
#
# # 处理注册的请求  POST
# @app.route('/register', methods=['POST'])
# def register():
#     form = request.get_json()
#     u = User(form)
#     r = {
#         'success': True,
#         'message': '登录成功',
#     }
#     status, msgs = u.valid()
#     if status:
#         u.save()
#         # r['success'] = True
#         # 下面这句可以在关闭浏览器后保持用户登录
#         session.permanent = True
#         session['username'] = u.username
#         r['next'] = url_for('timeline', username=u.username)
#     else:
#         r['success'] = False
#         r['message'] = '\n'.join(msgs)
#     return jsonify(r)


@app.route('/tweet/<username>')
def other_user_view(username):
    user = User.query.filter_by(username=username).first()
    print('debug username', username)
    print('debug user', user)
    view_user = current_user()
    all_tweets = user.tweets
    all_tweets.sort(key=lambda t: t.created_time, reverse=True)
    return render_template('other.html', user=user, view_user = view_user, all_tweets=all_tweets)


# @app.route('/timeline/<username>')
# def timeline(username):
#     data_u = User.query.filter_by(username=username).first()
#     cur_u = current_user()
#     if data_u is None:
#         abort(404)
#     elif data_u != cur_u:
#         abort(401)
#     else:
#         all_tweets = Tweet.query.all()
#         all_tweets.sort(key=lambda t: t.created_time, reverse=True)
#         return render_template('timeline.html', user=data_u, all_tweets=all_tweets)


# @app.route('/timeline', methods=['POST'])
# @app.route('/mytweet', methods=['POST'])
# def tweet_add():
#     user = current_user()
#     if user is None:
#         return redirect(url_for('login_view'))
#     else:
#         form = request.get_json()
#         t = Tweet(form)
#         t.user = user
#         t.save()
#         r = {
#             'success': True,
#             'message': '添加成功',
#             'data': t.json()
#         }
#         return jsonify(r)


# @app.route('/mytweet/<username>')
# def mytweet_view(username):
#     data_u = User.query.filter_by(username=username).first()
#     cur_u = current_user()
#     if data_u is None:
#         abort(404)
#     elif data_u != cur_u:
#         abort(401)
#     else:
#         all_tweets = cur_u.tweets
#         all_tweets.sort(key=lambda t: t.created_time, reverse=True)
#         return render_template('mytweet.html', user=data_u, all_tweets=all_tweets)


@app.route('/tweet/update/<tweet_id>')
def tweet_update_view(tweet_id):
    one_tweet = Tweet.query.filter_by(id=tweet_id).first()
    data_u = one_tweet.user
    cur_u = current_user()
    if data_u is None:
        abort(404)
    elif data_u != cur_u:
        abort(401)
    else:
        return render_template('tweet_update.html', tweet=one_tweet, user=current_user())


# @app.route('/tweet/update/<tweet_id>', methods=['POST'])
# def tweet_update(tweet_id):
#     one_tweet = Tweet.query.filter_by(id=tweet_id).first()
#     user = one_tweet.user
#     cur_u = current_user()
#     if user is None:
#         abort(404)
#     elif user != cur_u:
#         abort(401)
#     else:
#         form = request.form
#         one_tweet.update(form)
#         one_tweet.save()
#         return redirect(url_for('mytweet_view', username=user.username))


@app.route('/tweet/delete/<tweet_id>', methods=['POST'])
def tweet_delete(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first()
    if t is None:
        abort(404)
    user = current_user()
    if user is None or user.id != t.user_id:
        abort(401)
    else:
        t.delete()
        r = {
            'success': True,
            'message': '删除成功',
        }
        return jsonify(r)


@app.route('/tweet/comments/<tweet_id>')
def comments_view(tweet_id):
    view_user = current_user()
    one_tweet = Tweet.query.filter_by(id=tweet_id).first()
    user = one_tweet.user
    comments = one_tweet.comments
    comments.sort(key=lambda t: t.created_time, reverse=True)
    return render_template('comments.html', user=user, view_user = view_user, one_tweet=one_tweet, comments=comments)


# @app.route('/tweet/comments/<tweet_id>', methods=['POST'])
# def comment_add(tweet_id):
#     user = current_user()
#     tweet = Tweet.query.filter_by(id=tweet_id).first()
#     form = request.get_json()
#     print('debug form', form)
#     c = Comment(form)
#     c.user = user
#     c.tweet = tweet
#     c.save()
#     r = {
#         'success': True,
#         'message': '添加成功',
#         'data': c.json()
#     }
#     return jsonify(r)


db = SQLAlchemy()

# 待解决：
# jQ模板有点问题:看mytweet的模板
# 视图函数非常相似，如何简化
if __name__ == '__main__':
    # 数据库的路径
    db_path = './db.sqlite'
    # 获取 app 的实例
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'random string'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    # 这一行 加了就没 warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    db.app = app

    from api import api

    app.register_blueprint(api, url_prefix='/api')

    config = {
        'debug': True,
    }
    app.run(**config)
