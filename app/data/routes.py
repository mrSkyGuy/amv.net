from flask import redirect, render_template
from main import app


@app.route("/")
def root():
    return redirect("/feed")


@app.route("/feed")
def feed():
    return "feed"
