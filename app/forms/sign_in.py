from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired

from data.db_session import create_session
from data.models.users import User


class SignInForm(FlaskForm):
    username_or_email = StringField(
        "username/email", validators=[DataRequired("You missed the field")]
    )
    password = PasswordField(
        "password", validators=[DataRequired("You missed the field")]
    )
    remember_me = BooleanField("remember me")

    submit_sign_in = SubmitField("Continue")

    def validate_username_or_email(self, username_or_email):
        is_email = False
        if "@" in username_or_email.data:
            is_email = True

        session = create_session()

        if is_email:
            user = (
                session.query(User).filter(User.email == username_or_email.data).first()
            )
            if not user:
                raise ValidationError("User not found")
        else:
            user = (
                session.query(User)
                .filter(User.username == username_or_email.data)
                .first()
            )
            if not user:
                raise ValidationError("User not found")

        if not user.check_password(self.password.data):
            raise ValidationError("Invalid password")
