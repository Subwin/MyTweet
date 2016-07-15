from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 待解决：
# jQ模板有点问题:看mytweet的模板
# 视图函数非常相似，如何简化


def init_app():
    # 数据库的路径
    db_path = 'db.sqlite'
    # 获取 app 的实例
    app = Flask(__name__)
    app.secret_key = 'random string'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'random string'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    # 这一行 加了就没 warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    db.app = app

    from .api import api
    from .auth import blue as auth
    from .controllers import main

    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
