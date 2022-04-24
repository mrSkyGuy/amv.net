from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from data import db_session
from data.models.users import User
from data.api.videos_resource import VideosListResource, VideosResource
from data.api.users_resource import UsersListResource, UsersResource
import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

api = Api(app)
api.add_resource(VideosListResource, '/api/videos') 
api.add_resource(VideosResource, '/api/videos/<int:video_id>')
api.add_resource(UsersListResource, '/api/users')
api.add_resource(UsersResource, '/api/users/<int:user_id>')

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
