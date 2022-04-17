const videoPlayer = document.querySelector(".video-player")
const video = videoPlayer.querySelector('.video__content')
const playButton = videoPlayer.querySelector('.video-controls__play-button')
const volume = videoPlayer.querySelector('.video-controls__volume-range')
const volumeIcon = videoPlayer.querySelector('.volume-icon')
const currentTimeElement = videoPlayer.querySelector('.time__current-time')
const durationTimeElement = videoPlayer.querySelector('.time__duration')
const progress = videoPlayer.querySelector('.video-controls__progress-bar')
const progressBar = videoPlayer.querySelector('.video-controls__progress-bar-filled')


// Play and Pause button
playButton.addEventListener('click', e => {
    if (video.paused) {
      video.play()
      playButton.innerHTML = '<span class="material-icons-outlined">pause_circle</span>'
    } else {
      video.pause()
      playButton.innerHTML = '<span class="material-icons-outlined">play_circle</span>'
    }
  })
  
// Volume
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

// current time and duration
const currentTime = () => {
    let currentMinutes = Math.floor(video.currentTime / 60)
    let currentSeconds = Math.floor(video.currentTime - currentMinutes * 60)
    let durationMinutes = Math.floor(video.duration / 60)
    let durationSeconds = Math.floor(video.duration - durationMinutes * 60)

    currentTimeElement.innerHTML = `${currentMinutes}:${currentSeconds < 10 ? '0' + currentSeconds : currentSeconds}`
    durationTimeElement.innerHTML = `${durationMinutes}:${durationSeconds}`
}

video.addEventListener('timeupdate', currentTime)
video.addEventListener('click', () => {
  if (video.paused) {
    video.play()
    playButton.innerHTML = '<span class="material-icons-outlined">pause_circle</span>'
  } else {
    video.pause()
    playButton.innerHTML = '<span class="material-icons-outlined">play_circle</span>'
  }
})

// Progress bar
video.addEventListener('timeupdate', () =>{
  const percentage = (video.currentTime / video.duration) * 100
  progressBar.style.width = `${percentage}%`
})

// change progress bar on click
progress.addEventListener('click', e => {
  const progressTime = (e.offsetX / progress.offsetWidth) * video.duration
  video.currentTime = progressTime
})