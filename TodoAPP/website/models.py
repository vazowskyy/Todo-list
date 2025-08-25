from flask import current_app
from flask_login import UserMixin
from sqlalchemy import func
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    tasks = db.relationship('Task')

    def generate_reset_password_token(self):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

        return serializer.dumps(self.email, salt=self.password)

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @staticmethod
    def validate_reset_password_token(token: str, user_id: int):
        user = db.session. get(User, user_id)

        if user is None:
            return None

        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            token_user_email = serializer.loads(
                token,
                max_age=current_app.config["RESET_PASS_TOKEN_MAX_AGE"],
                salt=user.password,
            )

        except (BadSignature, SignatureExpired):
            return None

        if token_user_email != user.email:
            return None

        return user


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    text = db.Column(db.String(100), default="")
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    completed = db.Column(db.Boolean, default=False)
