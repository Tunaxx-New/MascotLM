import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication

from window.interfaces.iapp import IApp
from window.interfaces.imodel_behaviour import IModelBehaviour
from window.model_window import ModelWindow

class QtApp(IApp):
    def __init__(self, app: QApplication):
        self.app = app

    def start(self) -> None:
        sys.exit(self.app.exec_())


def create_app(width: int, height: int, web_port: int, show_hide_key: str, popup_timeout: int, popup_destoroy_key: str) -> (IModelBehaviour, IApp):
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseOpenGLES)
    app = QtApp(QtWidgets.QApplication(sys.argv))
    screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
    x = screen.right() - width - 8
    y = screen.bottom() - height - 8
    model_window = ModelWindow(x, y, width, height, web_port, show_hide_key, popup_timeout, popup_destoroy_key)
    model_window.show()
    return model_window, app
