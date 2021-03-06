const nextVideoSwitchButton = document.querySelector(".next-video-switch"),
      previousVideoSwitchButton = document.querySelector(".previous-video-switch")

const currentVideo = document.querySelector(".current-video"),
      currentVideoInfo = currentVideo.querySelector(".current-video__info"),
      currentVideoContent = currentVideo.querySelector(".video__content"),
      currentVideoAuthorLink = currentVideoInfo.querySelector(".author__link"),
      currentVideoAuthorAvatar = currentVideoInfo.querySelector(".author__avatar"),
      currentVideoAuthorNickname = currentVideoInfo.querySelector(".author__nickname"),
      currentVideoAuthorSubscribersCount = currentVideoInfo.querySelector(".subscribers__count"),
      currentVideoAuthorVideosCount = currentVideoInfo.querySelector(".videos__count"),
      currentVideoVideoViewsCount = currentVideoInfo.querySelector(".views__count"),
      currentVideoVideoLikeCount = currentVideoInfo.querySelector(".likes__count"),
      currentVideoVideoCommentsCount = currentVideoInfo.querySelector(".comments__count"),
      currentVideoDescription = currentVideo.querySelector(".current-video__description p")

const nextVideoContent = document.querySelector(".next-video .next-video__content"),
      previousVideoContent = document.querySelector(".previous-video .previous-video__content"),
      previousVideo = document.querySelector(".previous-video"),
      previousVideoSwitch = previousVideoSwitchButton.querySelector(".switch")


function sendRequest(method, url, body = null) {
    // Функция для AJAX запросов на сервер

    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest()
        xhr.open(method, url)

        xhr.responseType = "json"
        if (method.toLowerCase() == "post") {
            xhr.setRequestHeader("Content-Type", "application/json")
        }

        xhr.onload = () => {
            if (xhr.status >= 400) {
                reject(xhr.response)
            } else {
                resolve(xhr.response)
            }
        }

        xhr.onerror = () => reject(xhr.response)

        method.toLowerCase() == "post" ? 
            xhr.send(JSON.stringify(body)) 
            : xhr.send()
    })
} 


// Если переключаем на следующее видео
nextVideoSwitchButton.addEventListener("click", e => {
    const requestForSwitchCurrentVideo = sendRequest(  // Запрос на сервер для данных
        "post", "/ajax/get_next_video", {switch: true}  // *с переключением видео
    )
    requestForSwitchCurrentVideo.then(data => {
        if (data["is_start"]) {  
            // Если сервер сказал нам, что это начало ленты, то скрываем блок 
            // предыдущего видео и кнопку переключения
            previousVideoSwitchButton.style.opacity = 0
            previousVideoSwitch.style.cursor = 'default'
            previousVideo.style.opacity = 0
            reject()
        } else {
            // Иначе показываем все обратно
            previousVideoSwitchButton.style.opacity = 1
            previousVideoSwitch.style.cursor = 'pointer'
            previousVideo.style.opacity = 1
        }
        
        // Меняем содержимое текущего видео
        currentVideoContent.setAttribute("src", `../static/videos/${data["video_path"]}`)
        currentVideoContent.setAttribute("poster", `../static/previews/${data["preview_path"]}`)
        
        // Также меняем данные о видео
        currentVideoAuthorLink.setAttribute("href", `/${data["author_username"]}`)
        currentVideoAuthorAvatar.setAttribute("src", `../static/avatars/${data["author_avatar_path"]}`)
        currentVideoAuthorNickname.textContent = data["author_username"]
        currentVideoAuthorSubscribersCount.textContent = data["author_subscribers_count"]
        currentVideoAuthorVideosCount.textContent = data["author_videos_count"]

        currentVideoVideoViewsCount.textContent = data["views_count"]
        currentVideoVideoLikeCount.textContent = data["likes_count"]
        currentVideoVideoCommentsCount.textContent = data["comments_count"]

        currentVideoDescription.textContent = data["description"]

        // Если сервер нам говорит, что видео уже было лайкнуто пользователем, то показываем 
        // лайкнутую иконку 
        if (data["is_video_liked"]) {
            if (!likeButton.classList.contains("is-active")) likeButton.classList.add("is-active")
        } else {
            likeButton.classList.remove("is-active")
        }
    }).then(() => {
        // Следующим шагом меняем содержимое следующего видео (только превью)
        const requestForGetNextVideoPreview = sendRequest(
            "post", "/ajax/get_next_video", {switch: false}
        )
        requestForGetNextVideoPreview.then(data => {
            nextVideoContent.setAttribute("src", `../static/previews/${data["preview_path"]}`)
        })
    }).then(() => {
        // А также содержимое предыдущего видео
        const requestForGetPreviousVideoPreview = sendRequest(
            "post", "/ajax/get_previous_video", {switch: false}
        )
        requestForGetPreviousVideoPreview.then(data => {
            previousVideoContent.setAttribute("src", `../static/previews/${data["preview_path"]}`)
        })
    })
})

// Производим те же самые действия только для переключения на предыдущее видео
previousVideoSwitchButton.addEventListener("click", e => {
    const requestForSwitchCurrentVideo = sendRequest(
        "post", "/ajax/get_previous_video", {switch: true}
    )
    requestForSwitchCurrentVideo.then(data => {
        if (data["is_start"]) {
            previousVideoSwitchButton.style.opacity = 0
            previousVideoSwitch.style.cursor = 'default'
            previousVideo.style.opacity = 0
            reject()
        } else {
            previousVideoSwitchButton.style.opacity = 1
            previousVideoSwitch.style.cursor = 'pointer'
            previousVideo.style.opacity = 1
        }

        currentVideoContent.setAttribute("src", `../static/videos/${data["video_path"]}`)
        currentVideoContent.setAttribute("poster", `../static/previews/${data["preview_path"]}`)
        
        currentVideoAuthorLink.setAttribute("href", `/${data["author_username"]}`)
        currentVideoAuthorAvatar.setAttribute("src", `../static/avatars/${data["author_avatar_path"]}`)
        currentVideoAuthorNickname.textContent = data["author_username"]
        currentVideoAuthorSubscribersCount.textContent = data["author_subscribers_count"]
        currentVideoAuthorVideosCount.textContent = data["author_videos_count"]

        currentVideoVideoViewsCount.textContent = data["views_count"]
        currentVideoVideoLikeCount.textContent = data["likes_count"]
        currentVideoVideoCommentsCount.textContent = data["comments_count"]

        currentVideoDescription.textContent = data["description"]
        if (data["is_video_liked"]) {
            if (!likeButton.classList.contains("is-active")) likeButton.classList.add("is-active")
        } else {
            likeButton.classList.remove("is-active")
        }
    }).then(() => {
        const requestForGetNextVideoPreview = sendRequest(
            "post", "/ajax/get_next_video", {switch: false}
        )
        requestForGetNextVideoPreview.then(data => {
            nextVideoContent.setAttribute("src", `../static/previews/${data["preview_path"]}`)
        })
    }).then(() => {
        const requestForGetPreviousVideoPreview = sendRequest(
            "post", "/ajax/get_previous_video", {switch: false}
        )
        requestForGetPreviousVideoPreview.then(data => {
            if (data["is_start"]) {
                previousVideoSwitchButton.style.opacity = 0
                previousVideoSwitch.style.cursor = 'default'
                previousVideo.style.opacity = 0
                reject()
            } else {
                previousVideoSwitchButton.style.opacity = 1
                previousVideoSwitch.style.cursor = 'pointer'
                previousVideo.style.opacity = 1
            }

            previousVideoContent.setAttribute("src", `../static/previews/${data["preview_path"]}`)
        })
    })
})

// Переключение видео нажатием на кнопки-стрелки
document.addEventListener("keyup", e => {
    if (e.code == "ArrowRight" ) nextVideoSwitchButton.click()
})

document.addEventListener("keyup", e => {
    if (e.code == "ArrowLeft" ) previousVideoSwitchButton.click()
})
