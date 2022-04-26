const likeButton = document.querySelector(".lcssd__like")
const likesCount = document.querySelector(".likes__count")


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


document.addEventListener("DOMContentLoaded", () => {
    likeButton.addEventListener('click', () => {
        if (likeButton.classList.contains("is-active")) {
            const requestForLikeVideo = sendRequest('GET', "/ajax/dislike_current_video")
            requestForLikeVideo.then(data => {
                likeButton.classList.remove("is-active")
                likesCount.textContent = data["current_likes"]
            })
        } else {
            const requestForDislikeVideo = sendRequest('GET', "/ajax/like_current_video")
            requestForDislikeVideo.then(data => {
                likeButton.classList.add("is-active")
                likesCount.textContent = data["current_likes"]
            })
        }
    })
})