from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import jsonify
from flask import session
from flask import abort


from models import User
from models import Tweet

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


# 显示登录界面的函数  GET
@app.route('/login')
def login_view():
    template = 'login.html'
    return render_template(template)


# 处理登录请求  POST
@app.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    username = form.get('username', '')
    user = User.query.filter_by(username=username).first()
    r = {
        'success': True,
        'message': '登录成功',
    }
    if user is not None and user.validate_auth(form):
        r['success'] = True
        r['next'] = url_for('timeline', username=user.username)
        session.permanent = True
        session['username'] = username
    else:
        r['success'] = False
        r['message'] = '登录失败'
    return jsonify(r)


# 处理注册的请求  POST
@app.route('/register', methods=['POST'])
def register():
    form = request.get_json()
    u = User(form)
    r = {
        'success': True,
        'message': '登录成功',
    }
    status, msgs = u.valid()
    if status:
        u.save()
        # r['success'] = True
        # 下面这句可以在关闭浏览器后保持用户登录
        session.permanent = True
        session['username'] = u.username
        r['next'] = url_for('timeline', username=u.username)
    else:
        r['success'] = False
        r['message'] = '\n'.join(msgs)
    return jsonify(r)


@app.route('/timeline/<username>')
def timeline(username):
    data_u = User.query.filter_by(username=username).first()
    cur_u = current_user()
    if data_u is None:
        abort(404)
    elif data_u != cur_u:
        abort(401)
    else:
        all_tweets = Tweet.query.all()
        all_tweets.sort(key=lambda t: t.created_time, reverse=True)
        return render_template('timeline.html', user=data_u, all_tweets=all_tweets)


@app.route('/timeline', methods=['POST'])
def timeline_add():
    user = current_user()
    if user is None:
        return redirect(url_for('login_view'))
    else:
        form = request.get_json()
        t = Tweet(form)
        t.user = user
        t.save()
        r = {
            'success': True,
            'message': '添加成功',
            'data': t.json()
        }
        return jsonify(r)


@app.route('/mytweet/<username>')
def mytweet_view(username):
    data_u = User.query.filter_by(username=username).first()
    cur_u = current_user()
    if data_u is None:
        abort(404)
    elif data_u != cur_u:
        abort(401)
    else:
        t_user = current_user()
        all_tweets = t_user.tweets
        # all_tweets = Tweet.query.filter_by(username=username)
        all_tweets.sort(key=lambda t: t.created_time, reverse=True)
        return render_template('mytweet.html', user=data_u, all_tweets=all_tweets)


@app.route('/mytweet', methods=['POST'])
def mytweet():
    user = current_user()
    if user is None:
        return redirect(url_for('login_view'))
    else:
        form = request.get_json()
        t = Tweet(form)
        t.user = user
        t.save()
        r = {
            'success': True,
            'message': '添加成功',
            'data': t.json()
        }
        return jsonify(r)
# 两个页面留言板视图函数一样，如何简化？

# @app.route('/tweet/update/<tweet_id>')
# def tweet_update_view(tweet_id):
#     one_tweet = Tweet.query.filter_by(id=tweet_id).first()
#     return render_template('tweet_update.html', tweet=one_tweet, user=current_user())
#
#
# @app.route('/tweet/update/<tweet_id>', methods=['POST'])
# def todo_update(tweet_id):
#     form = request.form
#     one_todo = Tweet.query.filter_by(id=tweet_id).first()
#     user = one_todo.user
#     one_todo.update(form)
#     one_todo.save()
#     return redirect(url_for('tweet_add_view', username=user.username))


@app.route('/tweet/delete/<tweet_id>')
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


if __name__ == '__main__':
    config = {
        'debug': True,
    }
    app.run(**config)
