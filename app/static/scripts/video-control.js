const videoPlayer = document.querySelector(".video-player")
const video = videoPlayer.querySelector('.video__content')
const playButton = videoPlayer.querySelector('.video-controls__play-button')
const volume = videoPlayer.querySelector('.video-controls__volume-range')
const volumeIcon = videoPlayer.querySelector('.volume-icon')
const currentTimeElement = videoPlayer.querySelector('.time__current-time')
const durationTimeElement = videoPlayer.querySelector('.time__duration')
const progress = videoPlayer.querySelector('.video-controls__progress-bar')
const progressBar = videoPlayer.querySelector('.video-controls__progress-bar-filled')
const viewsCount = document.querySelector(".views__count")


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
  // Остановка видео при нажатии на кнопку
  playButton.addEventListener('click', e => {
      if (video.paused) {
        video.play()
        playButton.innerHTML = '<span class="material-icons-outlined">pause_circle</span>'
      } else {
        video.pause()
        playButton.innerHTML = '<span class="material-icons-outlined">play_circle</span>'
      }
    })
    
  // Громкость
  volume.addEventListener('mousemove', e => {
      video.volume = e.target.value
      if (video.volume >= 0.5) {
        volumeIcon.innerText = "volume_up"
      } else if (video.volume > 0) {
        volumeIcon.textContent = "volume_down"
      } else {
        volumeIcon.textContent = "volume_off"
      }
  })
  
  // Если мы нажали на иконку громкости, то переключаем между вкл и выкл режимами
  volumeIcon.addEventListener("click", () => {
    if (video.volume > 0) {
      video.volume = 0;
      volume.value = 0;
      volumeIcon.textContent = "volume_off"
    } else {
      video.volume = 0.5;
      volume.value = 0.5;
      volumeIcon.textContent = "volume_up"
    }
  })
  
  // Изменение время на видео
  const currentTime = () => {
      let currentMinutes = Math.floor(video.currentTime / 60)
      let currentSeconds = Math.floor(video.currentTime - currentMinutes * 60)
      let durationMinutes = Math.floor(video.duration / 60)
      let durationSeconds = Math.floor(video.duration - durationMinutes * 60)
  
      currentTimeElement.innerHTML = `${currentMinutes}:${currentSeconds < 10 ? '0' + currentSeconds : currentSeconds}`
      durationTimeElement.innerHTML = `${durationMinutes}:${durationSeconds}`
  }
  
  video.addEventListener('timeupdate', currentTime)

  // При нажатии на видео останавливаем
  video.addEventListener('click', () => {
    if (video.paused) {
      video.play()
      playButton.innerHTML = '<span class="material-icons-outlined">pause_circle</span>'
    } else {
      video.pause()
      playButton.innerHTML = '<span class="material-icons-outlined">play_circle</span>'
    }
  })
  
  // Прогресс бар
  let isVideoViewed = false
  video.addEventListener('timeupdate', () => {
    const percentage = (video.currentTime / video.duration) * 100
    progressBar.style.width = `${percentage}%`

    // Если видео началось заново, то сбрасываем
    if (percentage <= 5) isVideoViewed = false

    // Если пользователь просмотрел уже больше 20% процентов от видео, то увеличиваем счетчик просмотров
    if (percentage >= 20 && !isVideoViewed) {
      const requestForAddView = sendRequest('GET', '/ajax/add_view_to_current_video')
      requestForAddView.then(data => {
        // При получении ответа от сервера, увеличиваем счетчик просмотров
        viewsCount.textContent = data["current_views"]  // Сервер возвращает текущее количество просмотров
        isVideoViewed = true
      })
    }
  })
  
  // Перемещение по прогресс бару
  progress.addEventListener('click', e => {
    const progressTime = (e.offsetX / progress.offsetWidth) * video.duration
    video.currentTime = progressTime
  })
})