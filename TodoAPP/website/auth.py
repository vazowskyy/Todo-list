from flask import Blueprint, flash, render_template, request, session, url_for, redirect
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db
from werkzeug.security import check_password_hash, generate_password_hash
import re
from .forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = True if form.remember_me.data else False

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for("auth.login"))

        login_user(user=user, remember=remember)
        return redirect(url_for('views.todo_list'))
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data.lower().capitalize()
        email = form.email.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists', 'error')
            return redirect(url_for('auth.register'))

        password = form.password.data

        new_user = User(email=email, name=name, password=generate_password_hash(
            password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template("signup.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
