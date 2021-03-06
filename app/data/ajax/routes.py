from flask import jsonify, session, request
from flask_login import current_user

from random import sample

from main import app
from data.db_session import create_session
from data.models.videos import Video
from data.models.users import User


# Этот путь запроса служит для получения данных о следующем видео. И, при необходимости, 
# текущего видео; то есть, перелистывания
@app.route("/ajax/get_next_video", methods=["POST"])
def get_next_video():
    sess = create_session()
    videos = sess.query(Video).all()
    __video_indexes = [i for i in range(len(videos))]
    # Получаем случайную ленту. Точнее, случайные индексы для ленты. 
    # Если мы только зашли на сайт, то лента генерируется. В последующих разах, 
    # до тех пор, пока сессия не закроется, будет все та же лента
    if "feed_videos_indexes" not in session.keys():
        session["feed_videos_indexes"] = sample(__video_indexes, len(__video_indexes))
    feed_videos_indexes = session["feed_videos_indexes"]

    # Получаем текущий индекс видео из сессий
    current_video_index = session.get("current_video_index", -1)
    current_video_index += 1

    current_video = videos[
        feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
    ]

    if not request.json.get("switch", False):
        # Если нам в параметрах запроса сказали, что переключать видео не надо
        # (то есть, оставить индекс прежним), то возвращаем следующее видео, без
        # изменения индекса. То есть, говорим, что чел смотрит тот же видос.
        # Это нужно для блоков .previous-video и .next-video
        # Скорее всего данный запрос будет использоваться для получения превью
        # для блока .next-video__preview (либо в другом руте .previous-video__preview)

        response = current_video.to_dict(only=("preview_path",))
        response["is_start"] = current_video_index == 0
        # is_start говорит клиенту, что мы в начале ленты и нет возможности переключится
        # на предыдущее видео

        return jsonify(response)

    # Если пользователь нажал на .next-video-switch
    # (либо в другом руте .previous-video-switch),
    # то изменяем текущий индекс видео на следующий
    session["current_video_index"] = current_video_index

    response = current_video.to_dict(
        only=(
            "video_path",
            "preview_path",
            "description",
            "views_count",
            "comments_count",
            "video_created",
        )
    )
    # Уточняем сведения об авторе
    sess = create_session()
    author = sess.query(User).get(
        current_video.author_id
    )
    response = {
        **response,
        "likes_count": len(sess.query(Video).get(current_video.id).likes),  
        # Напрямую не обращаюсь, так как вылезает ошибка 
        # (Нужно поменять конфигурацию модели (я уже поменял, но работает это только 
        # на новых видео, тк нужно чтобы бд была полностью обновлена))
        # sqlalchemy.orm.exc.DetachedInstanceError: Parent instance <Video at 0x2013fc99e20> is not bound to a Session; lazy load operation of attribute 'likes' cannot proceed (Background on this error at: https://sqlalche.me/e/14/bhk3)
        "author_avatar_path": author.avatar_image,
        "author_username": author.username,
        "author_subscribers_count": len(author.followers),
        "author_videos_count": len(author.videos),
        "is_start": current_video_index == 0
    }

    # Ниже мы проверяем, что если человек уже лайкнул это видео, то показывать 
    # соответствующий лайк на странице
    if current_user.is_authenticated:
        temp = list(
            filter(lambda video: video.id == current_video.id, current_user.liked_videos)
        )
        response["is_video_liked"] = len(temp) == 1
    else:
        response["is_video_liked"] = False

    return jsonify(response)


# Этот путь запроса служит для получения данных о предыдущем видео. И, при необходимости, 
# текущего видео; то есть, перелистывания
@app.route("/ajax/get_previous_video", methods=["POST"])
def get_previous_video():
    sess = create_session()
    videos = sess.query(Video).all()
    __video_indexes = [i for i in range(len(videos))]

    if "feed_videos_indexes" not in session.keys():
        session["feed_videos_indexes"] = sample(__video_indexes, len(__video_indexes))
    feed_videos_indexes = session["feed_videos_indexes"]

    current_video_index = session.get("current_video_index", 0)

    if current_video_index > 0:  # Если вернулись в начало, то дальше не уходим
        current_video_index -= 1
    else:
        # Говорим о том, что мы в начале ленты и дальше видео нет
        return jsonify({"is_start": True})
    
    current_video = videos[
       feed_videos_indexes[(current_video_index) % len(feed_videos_indexes)]
    ]

    if not request.json.get("switch", False):
        response = current_video.to_dict(only=("preview_path",))

        response["is_start"] = False
        return jsonify(response)

    session["current_video_index"] = current_video_index
    response =current_video.to_dict(
        only=(
            "video_path",
            "preview_path",
            "description",
            "views_count",
            "comments_count",
            "video_created",
        )
    )
    sess = create_session()
    author = sess.query(User).get(current_video.author_id)
    response = {
        **response,
        "likes_count": len(sess.query(Video).get(current_video.id).likes),
        "author_avatar_path": author.avatar_image,
        "author_username": author.username,
        "author_subscribers_count": len(author.followers),
        "author_videos_count": len(author.videos),
        "is_start": False
    }

    if current_user.is_authenticated:
        temp = list(
            filter(lambda video: video.id == current_video.id, current_user.liked_videos)
        )
        response["is_video_liked"] = len(temp) == 1
    else:
        response["is_video_liked"] = False

    return jsonify(response)


# Этот путь запроса служит для того, чтобы сохранить данные о том, что видео было кем-то 
# просмотрено. Я решил, что мы не будем сохранять данные о том, кто именно посмотрел 
# видео, а просто увеличивать счетчик. Скорее всего, я реализую это в дальнейших 
# обновлениях 
@app.route("/ajax/add_view_to_current_video")
def add_view_to_current_video():
    sess = create_session()
    videos = sess.query(Video).all()

    feed_videos_indexes = session["feed_videos_indexes"]
    current_video_index = session["current_video_index"]

    current_video = videos[
        feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
    ]
    current_video.views_count += 1

    sess.commit()

    return jsonify(
        {
            "success": True, 
            "current_views": current_video.views_count  # Отсылаем клиенту о просмотрах 
            #                                             на данный момент
        }
    )


# Этот путь запроса служит для того, чтобы сохранить данные о том, что видео было кем-то 
# лайкнуто. Я решил, в отличии от предыдущего пути, что мы будем сохранять данные о том, 
# кто именно посмотрел лайкнул видео. Поэтому, лайк от неавторизованного юзера не 
# засчитывается => счетчик лайков останется не тронутым
@app.route("/ajax/like_current_video")
def like_current_video():
    sess = create_session()
    videos = sess.query(Video).all()

    feed_videos_indexes = session["feed_videos_indexes"]
    current_video_index = session["current_video_index"]

    current_video = videos[
        feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
    ]

    if current_user.is_authenticated:
        sess = create_session()

        cuser = sess.query(User).get(current_user.id)
        cvideo = sess.query(Video).get(current_video.id)
        cvideo.likes.append(cuser)  # Добавляем лайк к видео. 
        # Тем самым, благодаря SQLAlchemy, у нас, к тому же, пополнится список лайкнутых 
        # видео у самого пользователя
        sess.commit()

        return jsonify({"success": True, "current_likes": len(cvideo.likes)})

    return jsonify({"success": False})


@app.route("/ajax/dislike_current_video")
def dislike_current_video():
    sess = create_session()
    videos = sess.query(Video).all()

    feed_videos_indexes = session["feed_videos_indexes"]
    current_video_index = session["current_video_index"]

    current_video = videos[
        feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
    ]

    if current_user.is_authenticated:
        if current_user in current_video.likes:
            sess = create_session()

            cuser = sess.query(User).get(current_user.id)
            cvideo = sess.query(Video).get(current_video.id)
            cvideo.likes.remove(cuser)

            sess.commit()
        return jsonify({"success": True, "current_likes": len(cvideo.likes)})

    return jsonify({"success": False})


# Этот путь запроса нужен для подписки и отписки пользователя
@app.route("/ajax/follow_user", methods=["POST"])
def follow_user():
    if current_user.is_authenticated:
        sess = create_session()
        author_username = request.json.get("userName")
        author = sess.query(User).filter(User.username == author_username).first()
        temp = list(filter(lambda user: user.id == current_user.id, author.followers))
        cuser = sess.query(User).get(current_user.id)
        if request.json.get("unfollow"):
            if len(temp) == 1:
                author.followers.remove(cuser)
                sess.commit()
                return jsonify({"success": True, "followers_count": len(author.followers)})
            return jsonify({"success": False})
        
        if len(temp) != 0:
            return jsonify({"success": False})
        author.followers.append(cuser)
        sess.commit()
        return jsonify({"success": True, "followers_count": len(author.followers)})
    return jsonify({"success": False})
