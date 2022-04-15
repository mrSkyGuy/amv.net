from flask import redirect, render_template

from main import app
from forms.sign_up import SignUpForm


@app.route("/")
def root():
    return redirect("/feed")


@app.route("/feed")
def feed():
    return render_template("feed.html")


@app.route("/sign-up-in", methods=['GET', 'POST'])
def test():
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        return redirect("/feed")
    return render_template("sign-up-in.html", sign_up_form=sign_up_form)
