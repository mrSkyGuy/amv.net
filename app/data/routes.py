from flask import redirect, render_template
from main import app


@app.route("/")
def root():
    return redirect("/feed")


@app.route("/feed")
def feed():
    return render_template("feed.html")


@app.route("/sign-up-in")
def test():
    return render_template("sign-up-in.html")
