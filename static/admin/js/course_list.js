const timeTd = document.querySelectorAll(".time");
const menuBtn = document.querySelector(".menu_btn");
const mainHeader = document.querySelector(".main_header");

function paintingDate() {
    let today = new Date();
    let year = today.getFullYear();
    let month = today.getMonth() + 1;
    let date = today.getDate();
    let hours = today.getHours();
    let minutes = today.getMinutes();
    let seconds = today.getSeconds();

    let text1 = String(year) + "년 " + getStringDate(month) + "월 " + getStringDate(date) + "일";
    let text2 = getStringDate(hours) + ":" + getStringDate(minutes) + ":" + getStringDate(seconds);

    mainHeader.children[0].innerText = text1;
    mainHeader.children[2].innerText = text2;

    for (i = 0; i < timeTd.length; i++) {
        let lastTime = timeTd[i].parentNode.children[2].innerText;
        let count = 0;
        lastTime = lastTime.split("-");

        let day = Number(lastTime[2]) - date;
        let hour = Number(lastTime[3]) - hours;
        let minute = Number(lastTime[4]) - minutes;
        let second = 60 - seconds;

        text = getStringDate(day) + "일 " + getStringDate(hour) + "시간 " + getStringDate(minute) + "분 " + getStringDate(second) + "초";
        timeTd[i].parentNode.children[1].innerText = text;
    }
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