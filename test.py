import requests

host = 'http://127.0.0.1:5000'


def test_regist():
    url = host + '/register'
    account = dict(
        username='gua',
        password='gua',
    )
    r = requests.post(url,json=account)
    assert r.status_code == 200
    assert r.json()['success'], '注册失败'


def test_login():
    url = host + '/login'
    account = dict(
        username='gua',
        password='gua'
    )
    r = requests.post(url, json=account)
    # r发送了请求，自己有接受了请求？
    assert r.status_code == 200
    assert r.json()['success'], '登陆失败'
    print(r.json()['next'])


def test():
    # test_regist()
    test_login()

if __name__ == '__main__':
    test()


