const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("kangbao", {
    toggle: () => ipcRenderer.send("toggle"),

    setCps: (value) => ipcRenderer.send("set-cps", value),

    minimize: () => ipcRenderer.send("window-minimize"),

    close: () => ipcRenderer.send("window-close"),

    onStatus: (callback) => {
        ipcRenderer.on("status", (_, value) => callback(value));
    },

    onClick: (callback) => {
        ipcRenderer.on("do-click", callback);
    }
});