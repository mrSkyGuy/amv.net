from datetime import datetime
import sqlalchemy
import sqlalchemy.orm as orm
from ..db_session import SqlAlchemyBase


class Video(SqlAlchemyBase):
    __tablename__ = "videos"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    video_path = sqlalchemy.Column(sqlalchemy.String)

    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    author = orm.relation("User")