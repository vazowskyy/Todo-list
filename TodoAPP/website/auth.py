from flask import Blueprint, flash, render_template, request, session, url_for, redirect, render_template_string
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
from werkzeug.security import check_password_hash, generate_password_hash
import re
from .forms import RegistrationForm, LoginForm, ResetPasswordForm, FinalResetPasswordForm
from .templates.security.reset_password_email_content import (
    reset_password_email_html_content)
from flask_mailman import EmailMessage

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


@auth.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = request.form.get('email')

        user = user = User.query.filter_by(email=email).first()
        if user:
            send_reset_password_email(user)
        flash("Email with link to reset password has been sent if the email is in our database")

        return redirect(url_for("auth.forgot_password"))

    return render_template('security/forgot_password.html', form=form)


def send_reset_password_email(user):
    reset_password_url = url_for(
        "auth.reset_password",
        token=user.generate_reset_password_token(),
        user_id=user.id
    )
    email_body = render_template_string(
        reset_password_email_html_content, reset_password_url=reset_password_url
    )

    message = EmailMessage(
        subject="Reset your password",
        body=email_body,
        to=[user.email],
    )

    message.content_subtype = "html"

    message.send()


@auth.route("/reset_password/<token>/<int:user_id>", methods=['GET', 'POST'])
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    user = User.validate_reset_password_token(token, user_id)
    if not user:
        return render_template(
            "security/reset_password_error.html"
        )

    form = FinalResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(
            form.password.data, method='pbkdf2:sha256')
        db.session.commit()

        return render_template("security/reset_password_success.html")

    return render_template("security/reset_password.html", form=form)
