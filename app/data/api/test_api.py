import requests
from pprint import pprint


def get_byte_video(abs_path):
    with open(abs_path, "rb") as f:
        return f.read()


# pprint(requests.get("http://127.0.0.1:8080/api/videos").json())
# pprint(requests.get("http://127.0.0.1:8080/api/videos/1").json())

# pprint(
#     requests.post(
#         "http://127.0.0.1:8080/api/videos",
#         json={
#             "username": "SkyGuy", 
#             "password": 123123123,
#             "video": get_byte_video("C:/Users/nurma/Приложения/Telegram Desktop/video_2022-04-22_19-52-12.mp4"),
#             "video_extension": "mp4",
#             "description": "test video (loaded by api xD)"
#         },
#     )
# )
