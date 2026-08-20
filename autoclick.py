import sys
import time
import threading
import ctypes

import pyautogui
import keyboard

from PySide6.QtCore import Qt, QTimer, QRect
from PySide6.QtGui import QColor, QPainter, QPainterPath, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)


# =========================================================
# AUTO CLICK ENGINE
# =========================================================

running = False
cps = 30
click_interval = 1 / cps


def click_loop():
    global running

    while running:
        pyautogui.click()
        time.sleep(click_interval)


def toggle_click():
    global running

    running = not running

    if running:
        threading.Thread(target=click_loop, daemon=True).start()

    window.update_status()


# =========================================================
# WINDOWS MICA
# =========================================================

def enable_mica(hwnd):
    try:
        DWMWA_SYSTEMBACKDROP_TYPE = 38
        DWMSBT_MAINWINDOW = 2

        value = ctypes.c_int(DWMSBT_MAINWINDOW)

        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_SYSTEMBACKDROP_TYPE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
    except Exception:
        pass


# =========================================================
# GLASS PANEL
# =========================================================

class GlassPanel(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(
            QRect(0, 0, self.width(), self.height()),
            22,
            22
        )

        painter.fillPath(
            path,
            QColor(37, 24, 62, 185)
        )

        painter.setPen(
            QColor(196, 181, 253, 35)
        )

        painter.drawPath(path)


# =========================================================
# MAIN WINDOW
# =========================================================

class AutoClick(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("KangBao AutoClick")

        self.setFixedSize(470, 610)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Window
        )

        self.old_pos = None

        self.build_ui()

        QTimer.singleShot(
            100,
            lambda: enable_mica(int(self.winId()))
        )

    # -----------------------------------------------------

    def build_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(28, 25, 28, 22)
        root.setSpacing(15)

        # HEADER
        header = QHBoxLayout()

        title = QLabel("KangBao")
        title.setStyleSheet("""
            color: #f5f3ff;
            font-size: 25px;
            font-weight: 700;
        """)

        accent = QLabel(" AutoClick")
        accent.setStyleSheet("""
            color: #c4b5fd;
            font-size: 25px;
            font-weight: 400;
        """)

        header.addWidget(title)
        header.addWidget(accent)
        header.addStretch()

        close = QPushButton("×")
        close.setFixedSize(36, 36)
        close.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,15);
                color: #aaa2bd;
                border: none;
                border-radius: 18px;
                font-size: 20px;
            }

            QPushButton:hover {
                background: rgba(255,100,120,60);
                color: white;
            }
        """)

        close.clicked.connect(self.close)

        header.addWidget(close)

        root.addLayout(header)

        # STATUS
        status_panel = GlassPanel()
        status_layout = QVBoxLayout(status_panel)

        status_layout.setContentsMargins(22, 17, 22, 17)

        status_title = QLabel("STATUS")
        status_title.setStyleSheet("""
            color: #958ba9;
            font-size: 11px;
            font-weight: 700;
        """)

        self.status = QLabel("●  READY")
        self.status.setStyleSheet("""
            color: #aaa2bd;
            font-size: 15px;
            font-weight: 700;
        """)

        status_layout.addWidget(status_title)
        status_layout.addWidget(self.status)

        root.addWidget(status_panel)

        # CPS
        cps_panel = GlassPanel()
        cps_layout = QVBoxLayout(cps_panel)

        cps_layout.setContentsMargins(22, 18, 22, 20)

        cps_header = QHBoxLayout()

        cps_title = QLabel("CLICK SPEED")
        cps_title.setStyleSheet("""
            color: #958ba9;
            font-size: 11px;
            font-weight: 700;
        """)

        self.cps_label = QLabel("30 CPS")
        self.cps_label.setStyleSheet("""
            color: #c4b5fd;
            font-size: 14px;
            font-weight: 700;
        """)

        cps_header.addWidget(cps_title)
        cps_header.addStretch()
        cps_header.addWidget(self.cps_label)

        cps_layout.addLayout(cps_header)

        self.slider = QSlider(Qt.Horizontal)

        self.slider.setMinimum(1)
        self.slider.setMaximum(30)
        self.slider.setValue(30)

        self.slider.valueChanged.connect(self.change_cps)

        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(255,255,255,25);
                border-radius: 3px;
            }

            QSlider::sub-page:horizontal {
                background: #a78bfa;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                background: #ddd6fe;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
        """)

        cps_layout.addWidget(self.slider)

        root.addWidget(cps_panel)

        # RUN BUTTON
        self.run_button = QPushButton("RUN")

        self.run_button.setFixedHeight(65)

        self.run_button.clicked.connect(toggle_click)

        self.run_button.setStyleSheet("""
            QPushButton {
                background: #a78bfa;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 17px;
                font-weight: 700;
            }

            QPushButton:hover {
                background: #b9a3ff;
            }

            QPushButton:pressed {
                background: #8b5cf6;
            }
        """)

        root.addWidget(self.run_button)

        # SETTINGS
        settings = GlassPanel()
        settings_layout = QVBoxLayout(settings)

        settings_layout.setContentsMargins(22, 18, 22, 18)

        hotkey_title = QLabel("GLOBAL HOTKEY")

        hotkey_title.setStyleSheet("""
            color: #958ba9;
            font-size: 11px;
            font-weight: 700;
        """)

        hotkey = QLabel("F6")

        hotkey.setStyleSheet("""
            color: #f5f3ff;
            font-size: 17px;
            font-weight: 700;
        """)

        description = QLabel(
            "Press F6 anywhere to start or stop clicking"
        )

        description.setStyleSheet("""
            color: #8f879f;
            font-size: 10px;
        """)

        settings_layout.addWidget(hotkey_title)
        settings_layout.addWidget(hotkey)
        settings_layout.addWidget(description)

        root.addWidget(settings)

        root.addStretch()

        # FLOATING DOCK
        dock = QFrame()

        dock.setFixedHeight(62)

        dock.setStyleSheet("""
            QFrame {
                background: rgba(29,18,50,225);
                border: 1px solid rgba(196,181,253,35);
                border-radius: 31px;
            }
        """)

        dock_layout = QHBoxLayout(dock)

        dock_layout.setContentsMargins(18, 5, 18, 5)

        wolf = QLabel("🐺")

        wolf.setStyleSheet("""
            font-size: 25px;
            background: transparent;
        """)

        brand = QLabel("KangBaoOS")

        brand.setStyleSheet("""
            color: #f5f3ff;
            font-size: 12px;
            font-weight: 700;
            background: transparent;
        """)

        version = QLabel("AUTOCLICK")

        version.setStyleSheet("""
            color: #8f879f;
            font-size: 9px;
            background: transparent;
        """)

        dock_layout.addWidget(wolf)
        dock_layout.addSpacing(8)
        dock_layout.addWidget(brand)
        dock_layout.addStretch()
        dock_layout.addWidget(version)

        root.addWidget(dock)

    # -----------------------------------------------------

    def change_cps(self, value):
        global cps, click_interval

        cps = value
        click_interval = 1 / cps

        self.cps_label.setText(f"{cps} CPS")

    # -----------------------------------------------------

    def update_status(self):

        if running:
            self.status.setText("●  RUNNING")
            self.status.setStyleSheet("""
                color: #c4b5fd;
                font-size: 15px;
                font-weight: 700;
            """)

            self.run_button.setText("STOP")

        else:
            self.status.setText("●  READY")
            self.status.setStyleSheet("""
                color: #aaa2bd;
                font-size: 15px;
                font-weight: 700;
            """)

            self.run_button.setText("RUN")

    # -----------------------------------------------------
    # WINDOW DRAG
    # -----------------------------------------------------

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):

        if self.old_pos:

            current = event.globalPosition().toPoint()

            delta = current - self.old_pos

            self.move(self.pos() + delta)

            self.old_pos = current

    def mouseReleaseEvent(self, event):
        self.old_pos = None


# =========================================================
# START
# =========================================================

app = QApplication(sys.argv)

app.setStyle("Fusion")

window = AutoClick()
window.show()

keyboard.add_hotkey("f6", toggle_click)

sys.exit(app.exec())