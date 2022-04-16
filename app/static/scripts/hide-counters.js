const counters = document.querySelectorAll(".notifications__counter")
counters.forEach(counter => {
    if (counter.textContent == '0') {
        counter.style.display = 'none'
    }
})
