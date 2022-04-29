from flask import redirect, render_template, url_for, request, session, abort
from flask_login import current_user, login_user

from random import sample
from datetime import datetime
import os

from main import app

from data.db_session import create_session
from data.models.users import User
from data.models.videos import Video

from forms.sign_in import SignInForm
from forms.sign_up import SignUpForm
from forms.add_video import AddVideoForm


@app.route("/")
def root():
    return redirect(url_for("feed"))


# На данной странице расположена лента. Иначе говоря, это главная
@app.route("/feed")
def feed():
    sess = create_session()
    videos = sess.query(Video).all()  # Получаем все видео. Пока что это очень 
    #                                   неразумно - получать все сразу, но в дальнейшем я 
    #                                   исправлю это
    
    # Так как в сессиях не получается хранить список "videos", я решил хранить только индексы.
    # Да и так будет меньше нагружаться сессия
    __video_indexes = [i for i in range(len(videos))] 

    # Получаем текущую ленту
    if "feed_videos_indexes" not in session.keys():
        session["feed_videos_indexes"] = sample(__video_indexes, len(__video_indexes))
    feed_videos_indexes = session["feed_videos_indexes"]

    # Получаем текущий индекс видео из сессий
    if "current_video_index" not in session.keys():
        session["current_video_index"] = 0
    current_video_index = session["current_video_index"]

    # Текущее видео
    current_video = videos[
        feed_videos_indexes[current_video_index % len(feed_videos_indexes)]
    ]

    # Предыдущее видео. Если мы в начале ленты, то его нет - None
    previous_video = None
    if current_video_index > 0:
        previous_video = videos[
            feed_videos_indexes[(current_video_index - 1) % len(feed_videos_indexes)]
        ]

    # Следующее видео
    next_video = videos[
        feed_videos_indexes[(current_video_index + 1) % len(feed_videos_indexes)]
    ]


    return render_template(
        "feed.html", 
        current_video=current_video, 
        previous_video=previous_video,
        next_video=next_video,
        is_video_liked=len(
            list(
                filter(
                    lambda video: video.id == current_video.id, 
                    current_user.liked_videos
                )
            )
        ) == 1  # Есть ли текущее видео в лайкнутых видео пользователем
            if current_user.is_authenticated
            else False,
    )


# Страница регистрации и входа
@app.route("/sign_up_in", methods=["GET", "POST"])
def sign_up_in():
    sign_up_form = SignUpForm()
    sign_in_form = SignInForm()

    sess = create_session()
    if sign_up_form.submit_sign_up.data and sign_up_form.validate():
        # Из-за того, что на странице 2 формы нужно использовать такую проверку сабмита.
        # Чтобы при нажатии на один сабмит, второй не сработал и не проверилл свою форму
        # на валидацию

        user = User(username=sign_up_form.username.data, email=sign_up_form.email.data)
        user.set_password(sign_up_form.password.data)
        sess.add(user)
        sess.commit()

        return redirect(url_for("sign_up_in") + "?sign=in")

    if sign_in_form.submit_sign_in.data and sign_in_form.validate():
        if "@" in sign_in_form.username_or_email.data:
            user = (
                sess.query(User)
                .filter(User.email == sign_in_form.username_or_email.data)
                .first()
            )
        else:
            user = (
                sess.query(User)
                .filter(User.username == sign_in_form.username_or_email.data)
                .first()
            )

        if user.check_password(sign_in_form.password.data):
            login_user(user, remember=sign_in_form.remember_me.data)
            return redirect(url_for("feed"))

    return render_template(
        "sign-up-in.html",
        sign_up_form=sign_up_form,
        sign_in_form=sign_in_form,
        which_sign=request.args.get("sign", "up", str),  
        # which_sign - нужно, чтобы 
        # если пользователь, например, нажал на sign IN, то его сразу же 
        # перенаправило на нужный отдел
    )


# Страница пользователя
@app.route("/<username>")
def users(username):
    session = create_session()
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        abort(404)

    return render_template(
        "user.html", 
        user=user, 
        is_cuser_following=len(
            list(
                filter(
                    lambda u: u.id == current_user.id, 
                    user.followers
                )
            )
        ) == 1  # Подписан ли текущий пользователь на автора
            if current_user.is_authenticated
            else False
    )


@app.route("/add_video", methods=["GET", "POST"])
def add_video():
    if not current_user.is_authenticated:
        # Если юзер на авторизван, то отправляем его на соответствующую страницу
        return redirect("/sign_up_in?sign=in")
    add_video_form = AddVideoForm()

    if add_video_form.validate_on_submit():
        if "video" in request.files:
            video_file = request.files['video']  # Видео файл
            video_filename = (  # Название видео файла
                f"amv.net_video-{current_user.username}"
                + f"_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
                + f".{video_file.filename.split('.')[-1]}"
            )
            video_file.save(os.path.join("static/videos/", video_filename))  # Сохраняем на сервер

            if add_video_form.preview.data:
                if "preview" in request.files:
                    preview_file = request.files['preview']  # Превью файла, если пользователь его указал
                    preview_filename = f"{video_filename}_preview.{preview_file.filename.split('.')[-1]}"
                    preview_file.save(os.path.join("static/previews/", preview_filename))
            else:
                preview_filename = "default.png"  # Иначе дефолт
            description = add_video_form.description.data.strip()  # Описание для видео

            # Сохраняем в БД
            sess = create_session()
            cuser = sess.query(User).get(current_user.id)
            video = Video(
                video_path=video_filename,
                preview_path=preview_filename,
                description=description,
                author=cuser
            )
            sess.add(video)
            sess.commit()

            __video_indexes = [i for i in range(len(sess.query(Video).all()))]
            session["feed_videos_indexes"] = sample(__video_indexes, len(__video_indexes))

            return redirect(f"/{current_user.username}")

    return render_template("add-video.html", form=add_video_form)
