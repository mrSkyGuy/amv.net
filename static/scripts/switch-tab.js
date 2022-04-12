let buttonTab1 = document.querySelectorAll(".button-sign")[0],
    buttonTab2 = document.querySelectorAll(".button-sign")[1]

buttonTab1.addEventListener('click', () => {
    if (!(buttonTab1.classList.contains("selected-tab"))) {
        buttonTab1.classList.add("selected-tab")
        buttonTab2.classList.remove("selected-tab")
    }
})
buttonTab2.addEventListener('click', () => {
    if (!(buttonTab2.classList.contains("selected-tab"))) {
        buttonTab2.classList.add("selected-tab")
        buttonTab1.classList.remove("selected-tab")
    }
})


// document.addEventListener('DOMContentLoaded', () => {
//     document.querySelectorAll(".button-sign").forEach(
//         (item) => {
//             item.addEventListener("click", () => {
//                 if (item.classList.contains("selected-tab")) item.classList.remove("selected-tab")
//                 else item.classList.add("selected-tab")
//                 console.log(item.classList);
//             })
//         }
//     )
// })