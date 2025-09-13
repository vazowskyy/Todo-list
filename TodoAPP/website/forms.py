from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, EmailField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, Email


class RegistrationForm(FlaskForm):
    name = StringField(
        'Username', validators=[Length(min=4, max=25), InputRequired()])
    password = PasswordField('Password', validators=[Length(min=8, max=35), InputRequired(), EqualTo(
        'confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    email = EmailField("Email",  validators=[
                       InputRequired("Please enter your email address.")])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email(
        "This field requires a valid email address")])
    password = PasswordField("Password", validators=[
                             InputRequired()], id="password")
    remember_me = BooleanField("Remember me")


class ResetPasswordForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Email(
        "This field requires a valid email address")])
    submit = SubmitField("Request Password Reset")


class FinalResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[
                             InputRequired(), Length(min=8, max=32)])
    password2 = PasswordField("Repeat Password", validators=[
                              InputRequired(), EqualTo('password')])
    submit = SubmitField("Confirm Password Reset")


class TaskAddForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[Length(max=1000)])
    category = StringField("Category", validators=[Length(max=100)])


class TaskEditForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[Length(max=1000)])
    category = StringField("Category", validators=[Length(max=100)])
    completed = BooleanField("Completed?")


class TaskCategorySearch(FlaskForm):
    category = StringField("Filter by category: ")
    submit = SubmitField("Search")
