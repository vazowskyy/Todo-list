from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, EmailField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length


class RegistrationForm(FlaskForm):
    name = StringField(
        'Username', [validators.Length(min=4, max=25), InputRequired()])
    password = PasswordField('Password', [validators.Length(min=8, max=35), InputRequired(), EqualTo(
        'confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    email = EmailField("Email",  validators=[
                       InputRequired("Please enter your email address.")])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[
                             InputRequired()], id="password")
    remember_me = BooleanField("Remember me")


class ResetPasswordForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    submit = SubmitField("Request Password Reset")


class FinalResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[
                             InputRequired(), Length(min=8)])
    password2 = PasswordField("Repeat Password", validators=[
                              InputRequired(), EqualTo('password')])
    submit = SubmitField("Confirm Password Reset")


class TaskAddForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    content = StringField("Content")
    category = StringField("Category")


class TaskEditForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    content = StringField("Content")
    category = StringField("Category")
    completed = BooleanField("Completed?")


class TaskCategorySearch(FlaskForm):
    category = StringField("Filter by category: ")
    submit = SubmitField("Search")
