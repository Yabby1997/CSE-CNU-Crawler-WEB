const menuBtn = document.querySelector(".menu_btn");
const mainHeader = document.querySelector(".main_header");

function paintingDate() {
    let today = new Date();
    let year = today.getFullYear();
    let month = getStringDate(today.getMonth() + 1);
    let date = getStringDate(today.getDate());
    let hours = getStringDate(today.getHours());
    let minutes = getStringDate(today.getMinutes());
    let seconds = getStringDate(today.getSeconds());

    let text1 = String(year) + "년 " + month + "월 " + date + "일";
    let text2 = hours + ":" + minutes + ":" + seconds;

    mainHeader.children[0].innerText = text1;
    mainHeader.children[2].innerText = text2;
}

function getStringDate(date) {
    if (date < 10) {
        return "0" + String(date);
    } else {
        return String(date);
    }
}

function init() {
    menuBtn.addEventListener("click", function(e) {
        const menuHolder = document.querySelector(".menu_holder");
        const icon = e.target;
        if (menuHolder.classList.contains("hide")) {
            menuHolder.classList.remove("hide");
            icon.innerText = "highlight_off";
        } else {
            menuHolder.classList.add("hide");
            icon.innerText = "reorder";
        }
    })
    paintingDate();
    setInterval(paintingDate, 1000);
}

init();