const tabs = document.querySelectorAll('.button-sign')
const indicator = document.querySelector('.selected-tab-indicator')
const pages = [
    document.querySelector('.sign-up'), 
    document.querySelector('.sign-in')
]


tabs.forEach(tab => tab.addEventListener('click', e => {
    const tab = e.target
    const tabIndex = Array.prototype.indexOf.call(tab.parentNode.children, tab)
    const indicatorWidth = getComputedStyle(indicator).getPropertyValue('width')
    
    if (tabIndex == 0) {
        pages[0].classList.add('current-page')
        pages[1].classList.remove('current-page')
    } else if (tabIndex == 1) {
        pages[1].classList.add('current-page')
        pages[0].classList.remove('current-page')
    }
    indicator.style.transform = `translateX(calc( ${indicatorWidth} * ${tabIndex} + ${10 / 2 * tabIndex}px))`  // 10 - tab-space из sign-up-in.scss файла
    indicator.style.width = `calc(${indicatorWidth} + 2%)`
    setTimeout(() => indicator.style.width = indicatorWidth, 100)
}))