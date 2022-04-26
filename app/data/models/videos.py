from datetime import datetime
import sqlalchemy
import sqlalchemy.orm as orm
from ..db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Video(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "videos"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    video_path = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    preview_path = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, default="")

    views_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    comments_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    video_created = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())

    author_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False
    )
    author = orm.relation("User")

    def __repr__(self):
        return f"Video <id: {self.id}, video_path: {self.video_path}>"


""" 
    session = create_session()
    video1 = Video(
        video_path="video1.mp4",
        preview_path="video1_preview.png",
        description="Killua and Gon are my favorites #killua #gon #hxh",
        author=session.query(User).get(1)
    )
    session.add(video1)
    video2 = Video(
        video_path="video2.mp4",
        preview_path="video2_preview.png",
        description="Wooooow #fire",
        author=session.query(User).get(1)
    )
    session.add(video2)
    video3 = Video(
        video_path="video3.mp4",
        preview_path="video3_preview.png",
        description="Jujutsu kaisen the best #jujutsukaisen",
        author=session.query(User).get(1)
    )
    session.add(video3)
    video4 = Video(
        video_path="video4.mp4",
        preview_path="video4_preview.png",
        description="No comments #naruto #sasuke",
        author=session.query(User).get(1)
    )
    session.add(video4)
    video5 = Video(
        video_path="video5.mp4",
        preview_path="video5_preview.png",
        description="The most thrilling moment #deathnote #light #l",
        author=session.query(User).get(1)
    )
    session.add(video5)
    session.commit()
"""
