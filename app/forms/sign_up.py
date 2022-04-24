from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from werkzeug.security import check_password_hash, generate_password_hash

from data.models.users import User
from data.db_session import create_session
from string import ascii_letters


class SignUpForm(FlaskForm):
    username = StringField(
        "username",
        validators=[
            DataRequired("You missed the field"),
            Length(
                min=3,
                max=20,
                message="Username must be longer than 3 characters "
                + "and shorter than 20 characters",
            ),
        ],
    )
    email = EmailField(
        "email",
        validators=[
            DataRequired("You missed the field"),
            Email("It doesn't look like an email address 🤔"),
        ],
    )
    password = PasswordField(
        "password",
        validators=[
            DataRequired("You missed the field"),
            Length(min=8, message="Password must be longer 8 characters"),
        ],
    )
    password_again = PasswordField(
        "repeat password",
        validators=[
            DataRequired("You missed the field"),
            EqualTo("password", "Passwords don't match"),
        ],
    )

    submit_sign_up = SubmitField("Continue")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def validate_username(self, username):
        def check_symbols(string):
            available_symbols = ascii_letters + "1234567890_."
            for symbol in string:
                if symbol not in available_symbols:
                    return False
            return True

        if not check_symbols(username.data):
            raise ValidationError(
                "In your password must be only "
                + "lattin letters, numbers, dots and underlines"
            )

        if (
            create_session()
            .query(User)
            .filter(User.username.lower() == username.data.lower())
            .first()
        ):
            raise ValidationError("This username is already taken")

    def validate_email(self, email):
        if create_session().query(User).filter(User.email == email.data).first():
            raise ValidationError("This email is already taken")
