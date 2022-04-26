from flask import jsonify, session, request

from random import sample

from main import app
from data.db_session import create_session
from data.models.videos import Video
from data.models.users import User


sess = create_session()
videos = sess.query(Video).all()
__video_indexes = [i for i in range(len(videos))]


@app.route("/ajax/get_next_video", methods=["POST"])
def get_next_video():
    # Получаем случайную ленту
    if "feed_videos_indexes" not in session.keys():
        session["feed_videos_indexes"] = sample(__video_indexes, len(__video_indexes))
    feed_videos_indexes = session["feed_videos_indexes"]

    # Получаем текущий индекс видео из сессий
    current_video_index = session.get("current_video_index", -1)
    current_video_index += 1

    if not request.json.get("switch", False):
        # Если нам в параметрах запроса сказали, что переключать видео не надо
        # (то есть, оставить индекс прежним), то возвращаем следующее видео, без
        # изменения индекса. То есть, говорим, что чел смотрит тот же видос.
        # Это нужно для блоков .previous-video и .next-video
        # Скорее всего данный запрос будет использоваться для получения превью
        # для блока .next-video__preview (либо в другом руте .previous-video__preview)

        response = videos[
            feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
        ].to_dict(only=("preview_path",))

        if current_video_index == 0:
            response["is_start"] = True
        else:
            response["is_start"] = False

        return jsonify(response)

    # Если пользователь нажал на .next-video-switch
    # (либо в другом руте .previous-video-switch),
    # то изменяем текущий индекс видео на следующий
    session["current_video_index"] = current_video_index

    response = videos[
        feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
    ].to_dict(
        only=(
            "video_path",
            "preview_path",
            "description",
            "views_count",
            "likes_count",
            "comments_count",
            "video_created",
        )
    )
    # Уточняем сведения об авторе
    author = sess.query(User).get(
        videos[
            feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
        ].author_id
    )
    response["author_avatar_path"] = author.avatar_image
    response["author_username"] = author.username
    response["author_subscribers_count"] = author.subscribers_count
    response["author_videos_count"] = len(author.videos)

    if current_video_index == 0:
        response["is_start"] = True
    else:
        response["is_start"] = False

    return jsonify(response)


@app.route("/ajax/get_previous_video", methods=["POST"])
def get_previous_video():
    # Получаем случайную ленту
    if "feed_videos_indexes" not in session.keys():
        session["feed_videos_indexes"] = sample(__video_indexes, len(__video_indexes))
    feed_videos_indexes = session["feed_videos_indexes"]

    # Получаем текущий индекс видео из сессий
    current_video_index = session.get("current_video_index", 0)

    if current_video_index > 0:  # Если вернулись в начало, то дальше не уходим
        current_video_index -= 1
    else:
        # Говорим о том, что мы в начале ленты и дальше видео нет
        return jsonify({"is_start": True})

    if not request.json.get("switch", False):
        response = videos[
            feed_videos_indexes[(current_video_index) % len(feed_videos_indexes)]
        ].to_dict(only=("preview_path",))

        response["is_start"] = False
        return jsonify(response)

    session["current_video_index"] = current_video_index
    response = videos[
        feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
    ].to_dict(
        only=(
            "video_path",
            "preview_path",
            "description",
            "views_count",
            "likes_count",
            "comments_count",
            "video_created",
        )
    )
    author = sess.query(User).get(
        videos[
            feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
        ].author_id
    )
    response["author_avatar_path"] = author.avatar_image
    response["author_username"] = author.username
    response["author_videos_count"] = len(author.videos)
    response["author_subscribers_count"] = author.subscribers_count
    response["is_start"] = False

    return jsonify(response)


@app.route("/ajax/add_view_to_current_video")
def add_view_to_current_video():
    feed_videos_indexes = session["feed_videos_indexes"]
    current_video_index = session["current_video_index"]

    current_video = videos[
        feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
    ]

    current_video.views_count += 1
    print(current_video.views_count)
    # sess.commit()
    return jsonify({"success": True, "current_views": current_video.views_count})


@app.route("/ajax/like_current_video")
def like_current_video():
    feed_videos_indexes = session["feed_videos_indexes"]
    current_video_index = session["current_video_index"]

    current_video = videos[
        feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
    ]

    current_video.likes_count += 1
    # sess.commit()

    return jsonify({"success": True, "current_likes": current_video.likes_count})


@app.route("/ajax/dislike_current_video")
def dislike_current_video():
    feed_videos_indexes = session["feed_videos_indexes"]
    current_video_index = session["current_video_index"]

    current_video = videos[
        feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
    ]

    current_video.likes_count -= 1
    # sess.commit()

    return jsonify({"success": True, "current_likes": current_video.likes_count})
