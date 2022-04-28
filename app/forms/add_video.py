from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SubmitField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Length


class AddVideoForm(FlaskForm):
    video = FileField(  # Поле для загрузки видео файла
        "Load video",
        validators=[
            DataRequired("Video file is required"),  # Загрузить файл обязательно
            FileAllowed(
                ["mp4", "ogv", "webm"],  # Доступные форматы
                "amv.net doesn't support this video file extension",
            ),
        ],
    )
    preview = FileField(  # Поле для загрузки превью файла
        "Load preview",
        validators=[FileAllowed(["jpg", "png", "jpeg"])]
    )
    description = TextAreaField(  # Поле для описания видео
        "Add description",
        validators=[
            DataRequired("Description is required"),
            Length(min=10, max=100, message="Text must be from 10 to 100 characters"),
        ],
    )
    submit = SubmitField("Sumbit")
