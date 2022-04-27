from flask import jsonify
from flask_restful import Resource, reqparse

from string import ascii_letters

import requests

from ..db_session import create_session
from ..models.users import User
from .additional_funcs import abort_if_item_not_found


# Парсер аргументов для регистрации
parser_signup = reqparse.RequestParser()
parser_signup.add_argument("username", required=True)
parser_signup.add_argument("email", required=True)
parser_signup.add_argument("password", required=True)

# Парсер аргументов для авторизиции
parser_signin = reqparse.RequestParser()
parser_signin.add_argument("username", required=True)
parser_signin.add_argument("password", required=True)


class UsersResource(Resource):
    def get(self, user_id):
        """Получение пользователя по его ID"""

        abort_if_item_not_found(user_id, User)

        session = create_session()
        user = session.query(User).get(user_id)

        return jsonify(
            {
                "user": {
                    **user.to_dict(
                        only=("id", "username", "avatar_image", )
                    ),
                    "followers": [
                        follower.to_dict(only=("id", "username"))
                        for follower in user.followers
                    ],
                    "following": [
                        following.to_dict(only=("id", "username"))
                        for following in user.following
                    ]
                },
                "videos": [
                    {
                        "video": {
                            **video.to_dict(
                                only=(
                                    "id",
                                    "video_path",
                                    "preview_path",
                                    "description",
                                    "views_count",
                                    "comments_count",
                                    "video_created",
                                )
                            ),
                            "likes": [
                                user.to_dict(only=("id", "username"))
                                for user in video.likes
                            ]
                        }
                    }
                    for video in user.videos
                ],
                "success": True,
            }
        )

    def delete(self, user_id):
        """Удаление пользователя"""

        abort_if_item_not_found(user_id, User)

        args_signin = parser_signin.parse_args()  # Аргументы для аутентификации
        session = create_session()

        # ---------------------Проверям данные логина на валидность---------------------
        user = (
            session.query(User).filter(User.username == args_signin["username"]).first()
        )
        if not (user is None):
            if not (user.check_password(args_signin["password"])):
                return jsonify({"success": False, "message": "Invalid password"})
        else:
            return jsonify({"success": False, "message": "User not found"})

        # -----------------------------Удаляем пользователя-----------------------------
        session.delete(user)
        session.commit()

        return jsonify({"success": True})


class UsersListResource(Resource):
    def get(self):
        """Получение всех пользователей"""

        session = create_session()
        users = session.query(User).all()

        return jsonify(
            {
                "users": [
                    {
                        "user": {
                            **user.to_dict(
                                only=("id", "username", "avatar_image", )
                            ),
                            "followers": [
                                follower.to_dict(only=("id", "username"))
                                for follower in user.followers
                            ],
                            "following": [
                                following.to_dict(only=("id", "username"))
                                for following in user.following
                            ]
                        },
                        "videos": [
                            {
                                "video": {
                                    **video.to_dict(
                                        only=(
                                            "id",
                                            "video_path",
                                            "preview_path",
                                            "description",
                                            "views_count",
                                            "comments_count",
                                            "video_created",
                                        )
                                    ),
                                    "likes": [
                                        user.to_dict(only=("id", "username"))
                                        for user in video.likes
                                    ]
                                }
                            }
                            for video in user.videos
                        ],
                    }
                    for user in users
                ],
                "success": True,
            }
        )

    def post(self):
        """Регистрация пользователя"""

        args_signup = parser_signup.parse_args()
        session = create_session()

        # ----------------------------Проверяем на валидность---------------------------
        # username
        if not self.__check_username_length(args_signup["username"]):
            return jsonify(
                {
                    "success": False,
                    "message": "Username must be longer than 3 characters "
                    + "and shorter than 20 characters",
                }
            )
        if not self.__check_username_symbols(args_signup["username"]):
            return jsonify(
                {
                    "success": False,
                    "message": "In your password must be only "
                    + "lattin letters, numbers, dots and underlines",
                }
            )
        if not self.__check_username_not_in_db(args_signup["username"]):
            return jsonify(
                {"success": False, "message": "This username is already taken"}
            )

        # email
        if not self.__check_email_symbols(args_signup["email"]):
            return jsonify(
                {
                    "success": False,
                    "message": "This email doesn't look like an email address",
                }
            )
        if not self.__check_email_not_in_db(args_signup["email"]):
            print(self.__check_email_not_in_db(args_signup["email"]))
            return jsonify({"success": False, "message": "This email is already taken"})

        # password
        if not self.__check_password(args_signup["password"]):
            return jsonify(
                {"success": False, "message": "Password must be longer 8 characters"}
            )

        # --------------------------Регистрируем пользователя---------------------------
        user = User(username=args_signup["username"], email=args_signup["email"])
        user.set_password(args_signup["password"])
        session.add(user)
        session.commit()

        return jsonify(
            {
                "user": {
                    **user.to_dict(
                        only=("id", "username", "avatar_image", )
                    ),
                    "followers": [
                        follower.to_dict(only=("id", "username"))
                        for follower in user.followers
                    ],
                    "following": [
                        following.to_dict(only=("id", "username"))
                        for following in user.following
                    ]
                },
                "videos": [
                    {
                        "video": {
                            **video.to_dict(
                                only=(
                                    "id",
                                    "video_path",
                                    "preview_path",
                                    "description",
                                    "views_count",
                                    "comments_count",
                                    "video_created",
                                )
                            ),
                            "likes": [
                                user.to_dict(only=("id", "username"))
                                for user in video.likes
                            ]
                        }
                    }
                    for video in user.videos
                ],
                "success": True,
            }
        )

    def __check_username_length(self, username):
        """Проверка на длину username'а"""

        return 3 <= len(username) <= 20

    def __check_username_symbols(self, username):
        """Проверка на то, что username не содержим запрещенных символов"""

        available_symbols = ascii_letters + "1234567890_."
        for symbol in username:
            if symbol not in available_symbols:
                return False
        return True

    def __check_username_not_in_db(self, username):
        """Проверка на то, что username уже не занят кем-то другим"""

        session = create_session()
        user = session.query(User).filter(User.username == username).first()
        return user == None

    def __check_email_symbols(self, email):
        """Проверка на то, что email набран правильно"""

        email_parts = email.split("@")
        if len(email_parts) != 2:
            return False

        email_parts[1] = email_parts[1].split(".")
        if not (len(email_parts[1]) >= 2):
            return False

        for symb in email_parts[0]:
            if symb not in ascii_letters + "0123456789._":
                return False
        for part in email_parts[1]:
            for symb in part:
                if symb not in ascii_letters + "123456789":
                    return False

        return True

    def __check_email_not_in_db(self, email):
        """Проверка на то, что email свободен"""

        session = create_session()
        user = session.query(User).filter(User.email == email).first()
        return user is None

    def __check_password(self, password):
        """Проверка на длину пароля"""

        return len(password) >= 8
