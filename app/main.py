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
from data.models.users import User
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)
    # return User.query.get(user_id)


from data.routes import *


def main():
    db_session.global_init("db/db.sqlite")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG_MODE)

if __name__ == "__main__":
    main()