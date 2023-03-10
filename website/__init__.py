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
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:wkpProg219!@213.136.91.250:5432/zimtopup"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    db.app = app
    migrate = Migrate(app, db)

    # create the folders when setting up your app
    os.makedirs(os.path.join(app.instance_path, 'text_file_uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.instance_path, 'file_downloads'), exist_ok=True)

    # Create Database tables
    # Airtime Available
    try:
        conn = psycopg2.connect(database="zimtopup", user="postgres", password="wkpProg219!", host="213.136.91.250",
                                port="5432")
    except:
        print("Unable to connect to the database")

    cur = conn.cursor()
    try:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS airtime_available (id serial PRIMARY KEY, voucher_key varchar, serial_number varchar, batch_number varchar, denomination decimal, expiry_date timestamp, vic integer);")
    except:
        print("Can't drop our airtime_available database!")

    conn.commit()
    conn.close()
    cur.close()

    # Create Pinless Airtime Recharge
    try:
        conn = psycopg2.connect(database="zimtopup", user="postgres", password="wkpProg219!", host="213.136.91.250",
                                port="5432")
    except:
        print("Unable to connect to the database!")

    cur = conn.cursor()
    try:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS pinless_recharges (id serial PRIMARY KEY, reply_code integer, reply_message varchar, wallet_balance decimal, amount decimal, discount decimal, initial_balance decimal, final_balance decimal, validity_window timestamp, data decimal, sms integer, agent_reference varchar, recharge_id varchar);")
    except:
        print("Can't drop our pinless_recharges database!")

    conn.commit()
    conn.close()
    cur.close()

    # Create Data Bundle Recharge
    try:
        conn = psycopg2.connect(database="zimtopup", user="postgres", password="wkpProg219!", host="213.136.91.250",
                                port="5432")
    except:
        print("Unable to connect to the database!")

    cur = conn.cursor()
    try:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS data_bundles (id serial PRIMARY KEY, reply_code integer, reply_message varchar, wallet_balance decimal, amount decimal, discount decimal, initial_balance decimal, final_balance decimal, validity_window timestamp, data decimal, sms integer, agent_reference varchar, recharge_id varchar);")
    except:
        print("Can't drop our data_bundles database!")

    conn.commit()
    conn.close()
    cur.close()

    # Airtime Available
    try:
        conn = psycopg2.connect(database="zimtopup", user="postgres", password="wkpProg219!", host="213.136.91.250",
                                port="5432")
    except:
        print("Unable to connect to the database")

    cur = conn.cursor()
    try:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS airtime_sold (id serial PRIMARY KEY, voucher_key bigint, serial_number bigint, batch_number bigint, denomination decimal, expiry_date timestamp, vic integer, receiver varchar, buyer varchar);")
    except:
        print("Can't drop our airtime_sold database!")

    conn.commit()
    conn.close()
    cur.close()

    # User
    try:
        conn = psycopg2.connect(database="zimtopup", user="postgres", password="wkpProg219!", host="213.136.91.250",
                                port="5432")
    except:
        print("Unable to connect to the database")

    cur = conn.cursor()
    try:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS user (id serial PRIMARY KEY, email varchar, mobile varchar, password varchar, date_created timestamp, username varchar, role varchar, status boolean);")
    except:
        print("Can't drop user table!")

    conn.commit()
    conn.close()
    cur.close()

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
