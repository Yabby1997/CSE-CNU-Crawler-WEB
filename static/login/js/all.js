const menuBtn = document.querySelector(".menu_btn");
const mainHeader = document.querySelector(".main_header");
const refresh_btn = document.querySelector(".refresh_btn");

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

function loading() {
    const loading_text = document.querySelector(".loading_text");
    const long_time_text = document.querySelector(".long_time_text");
    let i = 0;
    let dot = ".";
    let text = "Loading";
    let time = 0;

    setInterval(function() {
        if (i !== 4) {
            i++;
        } else {
            i = 0;
        }
        let printText = text;
        for (k = 0; k < i; k++) {
            printText = printText + dot;
        }

        loading_text.innerText = printText;
    }, 700);

    setInterval(function() {
        if (time !== 20) {
            time++;
        } else {
            long_time_text.style.display = "block";
        }
    }, 1000)
}

function refresh_btn_handler() {
    refresh_btn.addEventListener("click", function(e) {
        document.querySelector(".loading_box").style.display = "flex";
        loading();
    });
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
    refresh_btn_handler();
    setInterval(paintingDate, 1000);
}

init();