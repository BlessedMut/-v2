from datetime import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)

def get_time_of_day(time):
    if time < 12:
        return "Morning"
    elif time < 16:
        return "Afternoon"
    elif time < 19:
        return "Evening"
    else:
        return "Evening"

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.status == None or user.status == False:
                flash("Account not verified, contact system Administrator.")
            elif check_password_hash(user.password, password):
                now = datetime.now()

                time_of_day = get_time_of_day(now.hour)
                flash(
                    f'Good {time_of_day.lower()} {user.username}! If you have any problems with the system, please send a ticket on blessedmutengwa@gmail.com or call +263 774 222 337',
                    category='success')
                login_user(user, remember=False)
                if user.role == "level_0":
                    return redirect(url_for('views.home'))
                elif user.role == "level_1":
                    return redirect(url_for('views.upload'))
                elif user.role == "level_2":
                    flash(
                        'This view is still under construction, please come again later. Sorry for the inconveniences caused',
                        category='warning')
                    return render_template("auth/login.html")
                    # return redirect(url_for('views.view_reports'))
                elif user.role == "level_3":
                    return redirect(url_for('views.download'))
            else:
                flash('Incorrect password, try again.', category='error')
                return render_template("auth/login.html")
        else:
            flash('Email does not exist.', category='error')
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('user_level')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif email.split("@")[1] != "zimtopup.com":
            flash("Email not in active directory. Please use emails under Zimtopup Domain.", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'), role=role)
            db.session.add(new_user)
            db.session.commit()
            # flash('Account created!', category='success')
            return render_template("auth/login.html")

    return render_template("auth/register.html")
