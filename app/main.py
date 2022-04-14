from flask import (
    Flask,
    render_template,
    redirect,
    request,
    jsonify,
    abort,
    make_response,
)
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)

from data import db_session
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


from data.routes import *


def main():
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG_MODE)

if __name__ == "__main__":
    main()