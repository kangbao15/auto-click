const runButton = document.getElementById("run");
const runText = document.getElementById("run-text");
const runIcon = document.getElementById("run-icon");

const statusText = document.getElementById("status-text");
const statusDot = document.getElementById("status-dot");

const slider = document.getElementById("slider");
const cps = document.getElementById("cps");

const minimize = document.getElementById("minimize");
const close = document.getElementById("close");


function setRunning(state) {

    if (state) {

        statusText.textContent = "RUNNING";

        statusDot.classList.add("running");

        runText.textContent = "STOP";

        runIcon.textContent = "■";

    } else {

        statusText.textContent = "READY";

        statusDot.classList.remove("running");

        runText.textContent = "RUN";

        runIcon.textContent = "▶";
    }
}


runButton.addEventListener("click", () => {
    window.kangbao.toggle();
});


slider.addEventListener("input", () => {

    const value = slider.value;

    cps.innerHTML = `${value} <span>CPS</span>`;

    window.kangbao.setCps(value);
});


minimize.addEventListener("click", () => {
    window.kangbao.minimize();
});


close.addEventListener("click", () => {
    window.kangbao.close();
});


window.kangbao.onStatus((state) => {
    setRunning(state);
});


setRunning(false);