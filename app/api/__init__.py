from flask import jsonify
from flask import session
from flask import Blueprint

from functools import wraps

# 包和文件夹概念不一样，这个在api包下，外层并没有包了，最高到api那一层，也就是.xx,如果用..xx就跳出包外了。
# 如果要引用的再包外，就直接from xx，我认为是包内包外同名模块不冲突。
from ..models import User

api = Blueprint('api', __name__)


def current_user():
    username = session.get('username', '')
    u = User.query.filter_by(username=username).first()
    return u


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            r = {
                'success': False,
                'message': '未登录',
            }
            return jsonify(r)
        return f(*args, **kwargs)
    return function


from . import tweet
from . import comment