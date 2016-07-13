from ..models import User
from ..models import Tweet
from . import api
from . import current_user
from . import login_required
from ..models import Comment

from flask import request
from flask import jsonify


@api.route('/tweet/comments/<tweet_id>', methods=['POST'])
def comment_add(tweet_id):
    user = current_user()
    tweet = Tweet.query.filter_by(id=tweet_id).first()
    form = request.get_json()
    print('debug form', form)
    c = Comment(form)
    c.user = user
    c.tweet = tweet
    c.save()
    r = {
        'success': True,
        'message': '添加成功',
        'data': c.json()
    }
    return jsonify(r)