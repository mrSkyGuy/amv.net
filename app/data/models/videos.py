from datetime import datetime
import sqlalchemy
import sqlalchemy.orm as orm
from ..db_session import SqlAlchemyBase


class Video(SqlAlchemyBase):
    __tablename__ = "videos"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    video_path = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    preview_path = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, default="")

    views_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    likes_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    comments_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    video_created = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())

    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    author = orm.relation("User")
