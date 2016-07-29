from ..models import Tweet
from . import api
from . import current_user
from ..models import Comment

from flask import url_for
from flask import request
from flask import jsonify


def add_extra(obj):
    # 这里的json啊，不是json模块那个json，是数据库类取类属性的。当初变量名没取好
    res = obj.json()
    extra = dict(
        username=obj.user.username,
        othertweet_view_url=url_for('controllers.other_tweet_view', username=obj.user.username),
    )
    res.update(extra)
    return res


@api.route('/tweet/comments/<tweet_id>', methods=['POST'])
def comment_add(tweet_id):
    user = current_user()
    tweet = Tweet.tweet_by_id(tweet_id)
    print('debug tweet_id', tweet_id)
    form = request.get_json()
    print('debug form', form)
    c = Comment(form)
    c.user = user
    c.tweet = tweet
    c.save()
    r = {
        'success': True,
        'message': '添加成功',
        'data': add_extra(c)
    }
    return jsonify(r)



'''
GET /api/comments/tweet_id
[
{
    'username': '111',
    'othertweet_view_url': 'url_for('controllers.other_tweet_view', username=t.user.username)',
    'creat_time': '123456',
    'comment_content': 'abcd',
}
]
'''


@api.route('/comments/<tweet_id>', methods=['GET'])
def get_comments(tweet_id):
    tweet = Tweet.query.filter_by(id=tweet_id).first_or_404()
    cs = tweet.comments
    r = dict(
        success=True,
        data=[add_extra(c) for c in cs],
    )
    return jsonify(r)