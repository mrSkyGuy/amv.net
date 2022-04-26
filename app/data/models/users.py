from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy

from datetime import datetime
from ..db_session import SqlAlchemyBase
from ..models.videos import Video
from sqlalchemy_serializer import SerializerMixin


followers = sqlalchemy.Table(
    "followers",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("author_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("follower_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
)

liked_videos = sqlalchemy.Table(
    "liked_videos",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column(
        "video_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("videos.id")
    ),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
)


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True, nullable=False)
    avatar_image = sqlalchemy.Column(sqlalchemy.String, default="avatar.jpg", nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    phone = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())

    videos = sqlalchemy.orm.relation("Video", back_populates="author")
    followers = sqlalchemy.orm.relation(
        "User",
        secondary="followers",
        primaryjoin=followers.c.author_id == id,
        secondaryjoin=followers.c.follower_id == id,
        backref="following"
    )
    liked_videos = sqlalchemy.orm.relation(
        "Video",
        secondary="liked_videos",
        primaryjoin=liked_videos.c.user_id == id,
        secondaryjoin=liked_videos.c.video_id == Video.id,
        backref="likes"
    )

    notifications_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    messages_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def __repr__(self):
        return f"User <id: {self.id}, username: {self.username}>"
