import requests
import json
from pprint import pprint


def get_byte_file(abs_path):
    with open(abs_path, "rb") as f:
        return f.read().decode("latin1")


# --------------------------------Проверка api для видео--------------------------------
# pprint(requests.get("http://127.0.0.1:8080/api/videos").json())
# pprint(requests.get("http://127.0.0.1:8080/api/videos/1").json())
# pprint(
#     requests.post(
#         "http://127.0.0.1:8080/api/videos",
#         json={
#             "username": "SkyGuy",
#             "password": 123123123,
#             "video": get_byte_file(
#                 "C:/Users/nurma/Приложения/Telegram Desktop/video_2022-04-22_19-52-12.mp4"
#             ),
#             "video_extension": "mp4",
#             "description": "test video (loaded by api xD)",
#         },
#     )
# )
# pprint(requests.delete(
#     "http://127.0.0.1:8080/api/videos/6",
#     json={
#         "username": "SkyGuy",
#         "password": "secret XDDDDD"
#     }
# ).json())

# --------------------------------Проверка api для юзера--------------------------------
# pprint(requests.get("http://127.0.0.1:8080/api/users").json())
# pprint(requests.get("http://127.0.0.1:8080/api/users/3").json())
# pprint(requests.post("http://127.0.0.1:8080/api/users", json={"username": "APIuser", "email": "alkjdfl@lkjasdf.ru", "password": "123123123"}).json())
# pprint(requests.delete("http://127.0.0.1:8080/api/users/3", json={"username": "APIuser", "password": 123123123}).json())
