// Скрипт, осуществляющий подписку и отписку пользователя

const followButton = document.querySelector(".follow")
const followersCount = document.querySelector(".followers-count")


function sendRequest(method, url, body = null) {
    // Функция для отправки запросов на сервер
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
    followButton.addEventListener("click", () => {
        if (followButton.classList.contains("is-following")) {
            const requestForUnfollowUser = sendRequest(
                "POST", 
                "/ajax/follow_user",
                {
                    userName: document.querySelector(".user__username > .username")
                        .textContent,
                    unfollow: true
                }
                // userName - username пользователя, с которым производятся действия
            )
            requestForUnfollowUser.then(data => {
                if (data["success"]) {
                    followButton.classList.remove("is-following")
                    followButton.textContent = "Follow"
                    followersCount.textContent = data["followers_count"]
                } else {
                    // Показывать сообщение, что нужно авторизоваться
                }
            })
        } else {
            const requestForFollowUser = sendRequest(
                "POST", 
                "/ajax/follow_user",
                {
                    userName: document.querySelector(".user__username > .username")
                        .textContent,
                    unfollow: false
                }
                // userName - username пользователя, с которым производятся действия
            )
            requestForFollowUser.then(data => {
                if (data["success"]) {
                    followButton.classList.add("is-following")
                    followButton.textContent = "Unfollow"
                    followersCount.textContent = data["followers_count"]
                } else {
                    // Показывать сообщение, что нужно авторизоваться
                }
            })
        }
    })
})
