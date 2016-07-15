from ..models import Tweet
from . import api
from . import current_user
from flask import request
from flask import jsonify
from flask import abort
from flask import redirect
from flask import url_for


@api.route('/tweet/add', methods=['POST'])
def tweet_add():
    u = current_user()
    form = request.get_json()
    t = Tweet(form)
    t.user = u
    t.save()
    r = dict(
        success=True,
        data=t.json(),
    )
    return jsonify(r)


@api.route('/tweet/update/<tweet_id>', methods=['POST'])
# @login_required
def tweet_update(tweet_id):
    one_tweet = Tweet.tweet_by_id(tweet_id)
    user = one_tweet.user
    cur_u = current_user()
    if user != cur_u:
        abort(401)
    else:
        form = request.form
        one_tweet.update(form)
        one_tweet.save()
        view = 'controllers.mytimeline_view'
        return redirect(url_for(view, username=user.username))


@api.route('/tweet/delete/<tweet_id>', methods=['POST'])
def tweet_delete(tweet_id):
    t = Tweet.tweet_by_id(tweet_id)
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
