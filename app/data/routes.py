from flask import redirect, render_template, url_for

from main import app, login_user
from data.db_session import create_session
from data.models.users import User
from forms.sign_in import SignInForm
from forms.sign_up import SignUpForm


@app.route("/")
def root():
    return redirect(url_for("feed"))


@app.route("/feed")
def feed():
    return render_template("feed.html")


@app.route("/sign_up_in", methods=["GET", "POST"])
def sign_up_in():
    sign_up_form = SignUpForm()
    sign_in_form = SignInForm()

    session = create_session()
    if sign_up_form.validate_on_submit():
        user = User(
            username=sign_up_form.username.data,
            email=sign_up_form.email.data
        )
        user.set_password(sign_up_form.password.data)
        session.add(user)
        session.commit()

        return redirect(url_for("feed"))

    if sign_in_form.validate_on_submit():
        if '@' in sign_in_form.username_or_email.data:
            user = session.query(User).filter(User.email == sign_in_form.username_or_email.data).first()
        else:
            user = session.query(User).filter(User.username == sign_in_form.username_or_email.data).first()

        if user.check_password(sign_in_form.password.data):
            login_user(user, remember=sign_in_form.remember_me.data)
            return redirect(url_for("feed"))
        
    return render_template(
        "sign-up-in.html", sign_up_form=sign_up_form, sign_in_form=sign_in_form
    )
