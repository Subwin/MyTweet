from app import models
from app import init_app


def rebuild_db():
    app = init_app()
    db = models.db
    db.drop_all()
    db.create_all()
    print('auth rebuild database')


def run():
    config = {
        'debug': True,
    }
    init_app().run(**config)


if __name__ == '__main__':
    rebuild_db()
    run()