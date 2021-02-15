const timeTd = document.querySelectorAll(".time");
const menuBtn = document.querySelector(".menu_btn");
const mainHeader = document.querySelector(".main_header");
const refresh_btn = document.querySelector(".refresh_btn");

function paintingDate() {
    let today = new Date();

    let m_year = today.getFullYear();
    let m_month = getStringDate(today.getMonth() + 1);
    let m_date = getStringDate(today.getDate());
    let m_hours = getStringDate(today.getHours());
    let m_minutes = getStringDate(today.getMinutes());
    let m_seconds = getStringDate(today.getSeconds());

    let text1 = String(m_year) + "년 " + m_month + "월 " + m_date + "일";
    let text2 = m_hours + ":" + m_minutes + ":" + m_seconds;

    mainHeader.children[0].innerText = text1;
    mainHeader.children[2].innerText = text2;



    for (i = 0; i < timeTd.length; i++) {
        let lastTime = timeTd[i].parentNode.children[2].innerText;
        lastTime = lastTime.split("-");

        let dataObj = new Date(lastTime[0], Number(lastTime[1]) - 1, lastTime[2], lastTime[3], lastTime[4], 59);
        let betweenDay = (dataObj.getTime() - today.getTime()) / 1000 / 60 / 60 / 24;
        betweenDay = Math.floor(betweenDay);
        let betweenTime = (dataObj.getTime() - today.getTime()) - (betweenDay * 24 * 60 * 60 * 1000);
        let hour = Math.floor(betweenTime / 1000 / 60 / 60);
        let minute = Math.floor((betweenTime - hour * 60 * 60 * 1000) / 1000 / 60);
        let second = Math.floor((betweenTime - hour * 60 * 60 * 1000 - minute * 60 * 1000) / 1000);
        let text = String(betweenDay) + "일 " + String(hour) + "시간 " + String(minute) + "분 " + String(second) + "초";
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