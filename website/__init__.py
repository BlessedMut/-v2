import os
from datetime import timedelta

import psycopg2
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

IMG_FOLDER = os.path.join('static', 'images')

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '^^*JHBsysvTV!*(&*U#)!(JKAskabsjhABSLJKSBJHA(!*(@*)!(*&^#%#$%&!'
    app.config["SESSION_PERMANENT"] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['MODIFIED'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:Support1999!@localhost:5432/zimtopup"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    db.app = app
    migrate = Migrate(app, db)

    # create the folders when setting up your app
    os.makedirs(os.path.join(app.instance_path, 'text_file_uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.instance_path, 'file_downloads'), exist_ok=True)

    os.makedirs(os.path.join('website', 'static', 'profiles', 'img'), exist_ok=True)

    UPLOAD_FOLDER = 'instance'
    app.config["STATIC_FOLDER"] = "website/static/"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, AirtimeSold, AirtimeAvailable

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
