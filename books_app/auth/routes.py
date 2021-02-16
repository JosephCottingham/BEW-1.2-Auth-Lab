from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from books_app.models import Book, Author, Genre, User
from books_app.auth.forms import SignUpForm, LoginForm
from books_app import bcrypt

# Import app and db from events_app package so that we can run app
from books_app import app, db

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signUpForm = SignUpForm
    if request.method == 'POST' and signUpForm.validate_on_submit():
        new_user = User(
            username=signUpForm.username,
            password=bcrypt.generate_password_hash(signUpForm.password)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect('main.homepage')
    return render_template('signup.html', signUpForm=signUpForm)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    signUpForm = SignUpForm
    if request.method == 'POST' and signUpForm.validate_on_submit():
        user = db.session.query(User).filter_by(username=signUpForm.username).first()
        if bcrypt.check_password_hash(user.password, signUpForm.password):
            login_user(user)
            return redirect('main.homepage')
    return render_template('login.html', signUpForm=signUpForm)

@auth.route('/logout')
def logout():
    logout_user(current_user)
    redirect('main.homepage')