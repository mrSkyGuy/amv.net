// Данный код прячем счетчики уведомлений, если их нет

const counters = document.querySelectorAll(".notifications__counter")

document.addEventListener("DOMContentLoaded", () => {
    counters.forEach(counter => {
        if (counter.textContent == '0') {
            counter.style.display = 'none'
        }
    })
})
