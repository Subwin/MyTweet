import requests
import json


host = 'http://127.0.0.1:5000'


def format_json(obj):
    return json.dumps(obj, indent=2)


def get(path):
    url = host + path
    print('url', url)
    r = requests.get(url)
    return r
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
def comments_list():
    path = '/api/comments/2'
    r = get(path)
    print('debug r', r, 'type r', type(r))
    response = r.json()
    data = response['data']
    # print('r', len(data))
    for d in data:
        print(format_json(d))

'''
GET /api/products
[
{
    'username': '111',
    'othertweet_view_url': 'url_for('controllers.other_tweet_view', username=t.user.username)',
    'created_time': '123456',
    'content': 'abcd',
    'tweet_comment_url': 'url_for('controllers.comments_view',tweet_id=t.id)',
    'comments_lenth': '111'
}
]
'''
def tweets_lists():
    path = '/api/tweets'
    r = get(path)
    print('debug r', r, 'type r', type(r))
    response = r.json()
    data = response['data']
    # print('r', len(data))
    for d in data:
        print(format_json(d))


def main():
    # tweets_lists()
    comments_list()

if __name__ == "__main__":
    main()