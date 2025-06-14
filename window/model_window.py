import keyboard
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWebChannel import QWebChannel

from window.bridges.drag_bridge import DragBridge
from window.interfaces.imodel_behaviour import IModelBehaviour
from window.speech_window import SpeechPopup


class ModelWindow(QtWidgets.QMainWindow):
    show_speech_signal = QtCore.pyqtSignal(str)

    def __init__(self, x, y, width, height, web_port, show_hide_key, popup_timeout: int, popup_destoroy_key: str):
        self.popup_timeout = popup_timeout
        self.popup_destoroy_key = popup_destoroy_key
        super().__init__()
        self.show_speech_signal.connect(self._on_show_speech)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(x, y, width, height)

        self.view = QtWebEngineWidgets.QWebEngineView(self)
        self.view.page().setBackgroundColor(QtCore.Qt.GlobalColor.transparent)
        self.view.setStyleSheet("background: transparent;")
        self.setCentralWidget(self.view)

        self.channel = QWebChannel()
        self.bridge = DragBridge(self)
        self.channel.registerObject("pyBridge", self.bridge)
        self.view.page().setWebChannel(self.channel)

        self.view.load(QtCore.QUrl(f"http://localhost:{web_port}"))

        self.view.installEventFilter(self)

        self.show_hide_key = show_hide_key
        self.transparent_mode = False
        self.mouse_inside_mode = False
        self.setMouseTracking(True)
        self.view.loadFinished.connect(self.disable_overlay)

        self.key_timer = QTimer()
        self.key_timer.timeout.connect(self.check_key_press)
        self.key_timer.start(100)

    def _on_show_speech(self, text: str):
        popup = SpeechPopup(text, self.popup_destoroy_key, parent=self, timeout=self.popup_timeout)
        popup.show_above_model_corner(self.view)

    def speech(self, text: str) -> None:
        self.show_speech_signal.emit(text)

    def check_key_press(self):
        if keyboard.is_pressed(self.show_hide_key):
            self.toggle_overlay()

    def enterEvent(self, event):
        self.mouse_inside_mode = True
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.mouse_inside_mode = False
        super().leaveEvent(event)

    def toggle_overlay(self):
        self.transparent_mode = not self.transparent_mode
        if self.transparent_mode:
            self.enable_overlay()
        else:
            self.disable_overlay()

    def enable_overlay(self):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowTransparentForInput)
        js = """
        document.body.style.opacity = 1.0;
        current_expression = 'neutral'
        model_.expression(current_expression);
        """
        self.view.page().runJavaScript(js)
        self.show()

    def disable_overlay(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowTransparentForInput)
        js = """
        document.body.style.opacity = 0.25;
        current_expression = 'sleepy'
        model_.expression(current_expression);
        """
        self.view.page().runJavaScript(js)
        self.show()

IModelBehaviour.register(ModelWindow)
