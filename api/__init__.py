from flask import jsonify
from flask import session
from flask import Blueprint

from functools import wraps

from ..models import User

api = Blueprint('api', __name__)


def current_user():
    # print('session, debug', session.permanent)
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

from . import tweet  #这一句为什么要放在最后？
from . import comment