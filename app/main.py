from flask import Flask
from flask_login import LoginManager

from data import db_session
from data.models.users import User
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/db.sqlite")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


from data.routes import *
from data.ajax.routes import *


def main():
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG_MODE)


if __name__ == "__main__":
    main()