from email.policy import default
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy

from datetime import datetime
from ..db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    avatar_image = sqlalchemy.Column(sqlalchemy.String, default="avatar.png")
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    phone = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())

    videos = sqlalchemy.orm.relation("Video", back_populates="author")
    notifications_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    messages_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
