const nextVideoSwitchButton = document.querySelector(".next-video-switch")
const previousVideoSwitchButton = document.querySelector(".previous-video-switch")
const currentVideoContent = document.querySelector(".current-video .video__content")
const nextVideoContent = document.querySelector(".next-video .next-video__content")
const previousVideoContent = document.querySelector(
    ".previous-video .previous-video__content"
)


function createRequest() {
    let Request = false

    if (window.XMLHttpRequest) {
        //Gecko-совместимые браузеры, Safari, Konqueror
        Request = new XMLHttpRequest()
    } else if (window.ActiveXObject) {
        //Internet explorer
        try {
             Request = new ActiveXObject("Microsoft.XMLHTTP")
        } catch (CatchException) {
             Request = new ActiveXObject("Msxml2.XMLHTTP")
        }
    }
 
    if (!Request) {
        console.error("Невозможно создать XMLHttpRequest")
    }
    
    return Request
} 


nextVideoSwitchButton.addEventListener("click", e => {
    const request = createRequest()
    request.open("POST", "/ajax/get_next_video")
    request.onload = () => {
        const response = request.responseText
        currentVideoContent.setAttribute("src", `../static/video/${response}`)
    }
    request.send()
})

previousVideoSwitchButton.addEventListener("click", e => {
    const request = createRequest()
    request.open("POST", "/ajax/get_previous_video")
    request.onload = () => {
        const response = request.responseText
        currentVideoContent.setAttribute("src", `../static/video/${response}`)
    }
    request.send()
})
