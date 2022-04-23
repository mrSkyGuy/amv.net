from datetime import datetime
from flask import jsonify
from flask_restful import Resource, reqparse
import werkzeug

from ..models.videos import Video
from ..models.users import User
from ..db_session import create_session
from .additional_funcs import abort_if_item_not_found


# Парсер аргументов для авторизиции
parser_login = reqparse.RequestParser()
parser_login.add_argument("username", required=True)
parser_login.add_argument("password", required=True)

# Парсер аргументов для загрузки видео
parser_video = reqparse.RequestParser()
parser_video.add_argument(
    "video", required=True, type=werkzeug.datastructures.FileStorage
)
parser_video.add_argument("video_extension", required=True)
parser_video.add_argument("preview", type=werkzeug.datastructures.FileStorage)
parser_video.add_argument("preview_extension")
parser_video.add_argument("description", required=False)


class VideosResource(Resource):
    def get(self, video_id):
        """Получение видео по его ID"""

        abort_if_item_not_found(video_id, Video)

        session = create_session()
        video = session.query(Video).get(video_id)

        response = {
            "video": video.to_dict(
                only=(
                    "id",
                    "video_path",
                    "preview_path",
                    "description",
                    "views_count",
                    "likes_count",
                    "comments_count",
                    "video_created",
                )
            ),
            "author": {
                "username": video.author.username,
                "videos_count": len(video.author.videos),
                "subscribers_count": video.author.subscribers_count,
            },
            "success": True,
        }

        return jsonify(response)

    def delete(self, video_id):
        """Удаление видео из своего аккаунта"""

        abort_if_item_not_found(video_id, Video)

        args_login = parser_login.parse_args()  # Аргументы для аутентификации
        session = create_session()

        # ---------------------Проверям данные логина на валидность---------------------
        user = (
            session.query(User).filter(User.username == args_login["username"]).first()
        )
        if not (user is None):
            if not (user.check_password(args_login["password"])):
                return jsonify({"success": False, "message": "Invalid password"})
        else:
            return jsonify({"success": False, "message": "User not found"})

        # Удаляем видео из аккаунта
        video = session.query(Video).get(video_id)
        session.delete(video)
        session.commit()

        return jsonify({"success": True})


class VideosListResource(Resource):
    def get(self):
        """Получение всех видео в базе данных"""

        session = create_session()
        videos = session.query(Video).all()

        response = {
            "videos": [
                {
                    "video": video.to_dict(
                        only=(
                            "id",
                            "video_path",
                            "preview_path",
                            "description",
                            "views_count",
                            "likes_count",
                            "comments_count",
                            "video_created",
                        )
                    ),
                    "author": {
                        "username": video.author.username,
                        "videos_count": len(video.author.videos),
                        "subscribers_count": video.author.subscribers_count,
                    },
                }
                for video in videos
            ],
            "success": True,
        }

        return jsonify(response)

    def post(self):
        """Добавление видео в свой аккаунт через API"""

        args_login = parser_login.parse_args()  # Аргументы для аутентификации
        session = create_session()

        # ---------------------Проверям данные логина на валидность---------------------
        user = (
            session.query(User).filter(User.username == args_login["username"]).first()
        )
        if not (user is None):
            if not (user.check_password(args_login["password"])):
                return jsonify({"success": False, "message": "Invalid password"})
        else:
            return jsonify({"success": False, "message": "User not found"})

        # ---------------------------Загрузка видео на сервис---------------------------
        args_video = parser_video.parse_args()  # Аргументы для загрузки видео

        video_file = args_video["video"]
        video_file_extension = args_video["video_extension"]
        preview_file = args_video.get("preview")
        preview_file_extension = args_video.get("preview_extension")
        description = args_video["description"]

        # Проверка на валидность данных
        # Видео
        if "." in video_file_extension:
            return jsonify(
                {
                    "success": False,
                    "message": "Please, give us video file extension (without dot)",
                }
            )
        if not self.__is_harmless_extensions(video_file_extension, file_type="video"):
            return jsonify(
                {
                    "success": False,
                    "message": f"We are not support the extension: {video_file_extension}",
                }
            )
        # Превью
        if preview_file is None:
            # preview_file = generate_preview(f.read())  # Эта функция в будущем
            # будет автоматически генерировать превью для видео. Пока что, ее нет

            preview_filename = "default.png"
        else:
            if (preview_file_extension is None) or ("." in preview_file_extension):
                return jsonify(
                    {
                        "success": False,
                        "message": "Please, give us preview file extension (without dot)",
                    }
                )
            elif not self.__is_harmless_extensions(
                preview_file_extension, file_type="photo"
            ):
                return jsonify(
                    {
                        "success": False,
                        "message": f"We are not support the extension: {preview_file_extension}",
                    }
                )

        # Сохраняем данные на сервер
        video_filename = (
            f"amv.net_video-{user.username}"
            + f"_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            + f".{video_file_extension}"
        )
        from os import getcwd

        print(getcwd())
        with open(f"static/videos/{video_filename}", "wb") as f:
            f.write(video_file.encode("latin1"))

        if not (preview_file is None):
            preview_filename = f"{video_filename}_preview.{preview_file_extension}"
            with open(f"static/previews/{preview_filename}", "wb") as f:
                f.write(preview_file.read())

        # Сохранение в БД
        video = Video(
            video_path=video_filename,
            preview_path=preview_filename,
            description=description,
            author=user,
        )
        session.add(video)
        session.commit()

        return jsonify(
            {
                "success": True,
                "result": {
                    "video": video.to_dict(
                        only=(
                            "id",
                            "video_path",
                            "preview_path",
                            "description",
                            "views_count",
                            "likes_count",
                            "comments_count",
                            "video_created",
                        )
                    ),
                    "author": {
                        "username": video.author.username,
                        "videos_count": len(video.author.videos),
                        "subscribers_count": video.author.subscribers_count,
                    },
                },
            }
        )

    def __is_harmless_extensions(self, extension, file_type):
        photo_extensions = ["jpg", "png", "jpeg"]
        video_extensions = ["mp4", "webm", "ogv"]

        if file_type.lower() == "photo":
            return extension in photo_extensions
        elif file_type.lower() == "video":
            return extension in video_extensions
