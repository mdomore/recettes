from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink


db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gu9OoQu6uxieponeiyae1phaMom4Ahviesho'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Meal, Tag, tags_association
    create_database(app)

    admin = Admin(app)
    admin.add_view(ModelView(Meal, db.session))
    admin.add_view(ModelView(Tag, db.session))

    with app.app_context():
        admin.add_link(MenuLink(name='List', category='', url='/'))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')

