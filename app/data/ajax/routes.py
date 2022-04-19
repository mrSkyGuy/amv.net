from flask import jsonify, session, request

from random import randrange

from main import app
from data.db_session import create_session
from data.models.videos import Video
from data.models.users import User


sess = create_session()
videos = sess.query(Video).all()


@app.route("/ajax/get_next_video", methods=["POST"])
def get_next_video():
    # Получаем текущий индекс видео из сессий 
    current_video_index = session.get(
        "current_video_index", randrange(0, len(videos) - 1)
    )
    current_video_index = (current_video_index + 1) % len(videos)

    if not request.json.get("switch", False):  
        # Если нам в параметрах запроса сказали, что переключать видео не надо 
        # (то есть, оставить индекс прежним), то возвращаем следующее видео, без 
        # изменения индекс. То есть говорим, что чел смотрит тот же видос. 
        # Это нужно для блоков .previous-video и .next-video
        # Скорее всего данный запрос будет использоваться для получения превью
        # для блока .next-video__preview (либо в другом руте .previous-video__preview)

        response = videos[current_video_index].to_dict(only=("preview_path", ))
        return jsonify(response)

    # Если пользователь нажал на .next-video-switch 
    # (либо в другом руте .previous-video-switch), 
    # то изменяем текущий индекс видео на следующий
    session["current_video_index"] = current_video_index

    response = videos[current_video_index].to_dict(
            only=(
                "video_path", "preview_path", "description", "views_count",
                "likes_count", "comments_count", "video_created"
            )
        )
    # Уточняем сведения об авторе
    author = sess.query(User).get(videos[current_video_index].author_id)
    response["author_avatar_path"] = author.avatar_image
    response["author_username"] = author.username
    response["author_subscribers_count"] = author.subscribers_count
    response["author_videos_count"] = len(author.videos)

    return jsonify(response)


@app.route("/ajax/get_previous_video", methods=["POST"])
def get_previous_video():
    current_video_index = session.get("current_video_index", 0)
    if current_video_index > 0:  # Если вернулись в начало, то дальше не уходим
        current_video_index -= 1

    if not request.json.get("switch", False):
        response = videos[current_video_index].to_dict(only=("preview_path", ))
        return jsonify(response)

    session["current_video_index"] = current_video_index
    response = videos[current_video_index].to_dict(
            only=(
                "video_path", "preview_path", "description", "views_count",
                "likes_count", "comments_count", "video_created"
            )
        )
    author = sess.query(User).get(videos[current_video_index].author_id)
    response["author_avatar_path"] = author.avatar_image
    response["author_username"] = author.username
    response["author_videos_count"] = len(author.videos)
    response["author_subscribers_count"] = author.subscribers_count

    return jsonify(response)
