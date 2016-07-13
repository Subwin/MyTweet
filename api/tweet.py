from ..models import User
from ..models import Tweet
from . import api
from . import current_user
from . import login_required

from flask import request
from flask import jsonify
from flask import abort
from flask import redirect
from flask import url_for


# main怎么到这里来了？
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
    one_tweet = Tweet.query.filter_by(id=tweet_id).first()
    user = one_tweet.user
    cur_u = current_user()
    # if user is None:
    #     abort(404)
    if user != cur_u:
        abort(401)
    else:
        form = request.form
        one_tweet.update(form)
        one_tweet.save()
        return redirect(url_for('mytweet_view', username=user.username)) #需要修改url


@api.route('/tweet/delete/<tweet_id>', methods=['POST'])
def tweet_delete(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first_or_404()
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
