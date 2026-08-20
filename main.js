const {
    app,
    BrowserWindow,
    globalShortcut,
    ipcMain
} = require("electron");

const path = require("path");
const koffi = require("koffi");

let win = null;
let clicking = false;
let cps = 30;
let clickTimer = null;


// ==========================================
// WINDOWS MOUSE API
// ==========================================

const user32 = koffi.load("user32.dll");

const mouse_event = user32.func(
    "void mouse_event(uint32 dwFlags, uint32 dx, uint32 dy, uint32 dwData, uintptr_t dwExtraInfo)"
);

const LEFTDOWN = 0x0002;
const LEFTUP = 0x0004;


function realClick() {

    mouse_event(
        LEFTDOWN,
        0,
        0,
        0,
        0
    );

    mouse_event(
        LEFTUP,
        0,
        0,
        0,
        0
    );
}


// ==========================================
// WINDOW
// ==========================================

function createWindow() {

    win = new BrowserWindow({
        width: 480,
        height: 650,
        icon: path.join(__dirname, "iconclick.png"),

        minWidth: 420,
        minHeight: 580,

        frame: false,
        transparent: true,
        resizable: true,

        backgroundColor: "#00000000",

        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            contextIsolation: true,
            nodeIntegration: false
        }
    });

    win.loadFile("index.html");

    win.on("closed", () => {
        win = null;
    });
}


// ==========================================
// AUTO CLICK
// ==========================================

function startClicking() {

    if (clicking) return;

    clicking = true;

    if (clickTimer) {
        clearInterval(clickTimer);
    }

    clickTimer = setInterval(() => {

        if (clicking) {
            realClick();
        }

    }, 1000 / cps);

    updateStatus();
}


function stopClicking() {

    clicking = false;

    if (clickTimer) {
        clearInterval(clickTimer);
        clickTimer = null;
    }

    updateStatus();
}


function toggleClicking() {

    if (clicking) {
        stopClicking();
    } else {
        startClicking();
    }
}


// ==========================================
// SEND STATUS TO UI
// ==========================================

function updateStatus() {

    if (!win) return;

    win.webContents.send(
        "status",
        clicking
    );
}


// ==========================================
// IPC
// ==========================================

ipcMain.on("toggle", () => {
    toggleClicking();
});


ipcMain.on("set-cps", (_, value) => {

    cps = Math.max(
        1,
        Math.min(30, Number(value))
    );

    if (clicking) {

        stopClicking();
        startClicking();

    }
});


ipcMain.on("window-minimize", () => {

    if (win) {
        win.minimize();
    }
});


ipcMain.on("window-close", () => {

    if (win) {
        win.close();
    }
});


// ==========================================
// START
// ==========================================

app.whenReady().then(() => {

    createWindow();

    const registered =
        globalShortcut.register(
            "F6",
            () => {

                console.log(
                    "F6 pressed"
                );

                toggleClicking();

            }
        );

    console.log(
        "KangBao AutoClick started"
    );

    console.log(
        "F6 registered:",
        registered
    );
});


// ==========================================
// CLEANUP
// ==========================================

app.on("will-quit", () => {

    globalShortcut.unregisterAll();

    if (clickTimer) {
        clearInterval(clickTimer);
        clickTimer = null;
    }

    clicking = false;
});