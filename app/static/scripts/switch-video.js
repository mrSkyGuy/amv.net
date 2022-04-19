const nextVideoSwitchButton = document.querySelector(".next-video-switch"),
      previousVideoSwitchButton = document.querySelector(".previous-video-switch")

const currentVideo = document.querySelector(".current-video"),
      currentVideoInfo = currentVideo.querySelector(".current-video__info"),
      currentVideoContent = currentVideo.querySelector(".video__content"),
      currentVideoAuthorAvatar = currentVideoInfo.querySelector(".author__avatar"),
      currentVideoAuthorNickname = currentVideoInfo.querySelector(".author__nickname"),
      currentVideoAuthorSubscribersCount = currentVideoInfo.querySelector(".subscribers__count"),
      currentVideoAuthorVideosCount = currentVideoInfo.querySelector(".videos__count"),
      currentVideoVideoViewsCount = currentVideoInfo.querySelector(".views__count"),
      currentVideoVideoLikeCount = currentVideoInfo.querySelector(".likes__count"),
      currentVideoVideoCommentsCount = currentVideoInfo.querySelector(".comments__count"),
      currentVideoDescription = currentVideo.querySelector(".current-video__description p")

const nextVideoContent = document.querySelector(".next-video .next-video__content"),
      previousVideoContent = document.querySelector(".previous-video .previous-video__content")


function sendRequest(method, url, body = null) {
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


nextVideoSwitchButton.addEventListener("click", e => {
    const requestForSwitchCurrentVideo = sendRequest(
        "post", "/ajax/get_next_video", {switch: true}
    )
    requestForSwitchCurrentVideo.then(data => {
        currentVideoContent.setAttribute("src", `../static/video/${data["video_path"]}`)
        currentVideoContent.setAttribute("poster", `../static/video/${data["preview_path"]}`)

        currentVideoAuthorAvatar.setAttribute("src", `../static/avatars/${data["author_avatar_path"]}`)
        currentVideoAuthorNickname.textContent = data["author_username"]
        currentVideoAuthorSubscribersCount.textContent = data["author_subscribers_count"]
        currentVideoAuthorVideosCount.textContent = data["author_videos_count"]

        currentVideoVideoViewsCount.textContent = data["views_count"]
        currentVideoVideoLikeCount.textContent = data["likes_count"]
        currentVideoVideoCommentsCount.textContent = data["comments_count"]

        currentVideoDescription.textContent = data["description"]
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
            previousVideoContent.setAttribute("src", `../static/previews/${data["preview_path"]}`)
        })
    })
})

previousVideoSwitchButton.addEventListener("click", e => {
    const requestForSwitchCurrentVideo = sendRequest(
        "post", "/ajax/get_previous_video", {switch: true}
    )
    requestForSwitchCurrentVideo.then(data => {
        currentVideoContent.setAttribute("src", `../static/video/${data["video_path"]}`)
        currentVideoContent.setAttribute("poster", `../static/video/${data["preview_path"]}`)

        currentVideoAuthorAvatar.setAttribute("src", `../static/avatars/${data["author_avatar_path"]}`)
        currentVideoAuthorNickname.textContent = data["author_username"]
        currentVideoAuthorSubscribersCount.textContent = data["author_subscribers_count"]
        currentVideoAuthorVideosCount.textContent = data["author_videos_count"]

        currentVideoVideoViewsCount.textContent = data["views_count"]
        currentVideoVideoLikeCount.textContent = data["likes_count"]
        currentVideoVideoCommentsCount.textContent = data["comments_count"]

        currentVideoDescription.textContent = data["description"]
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
            previousVideoContent.setAttribute("src", `../static/previews/${data["preview_path"]}`)
        })
    })
})
