from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication


class DragBridge(QObject):
    @pyqtSlot(int, int)
    def drag(self, dx, dy):
        win = QApplication.activeWindow()
        if win:
            win.move(win.x() + dx, win.y() + dy)
