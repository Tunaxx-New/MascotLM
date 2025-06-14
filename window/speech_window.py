import keyboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout


class SpeechPopup(QDialog):
    def __init__(self, text, destoroy_key: str, parent=None, timeout=3000):
        self.destroy_key = destoroy_key
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel()
        self.label.setText(text)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.label.setFont(QFont("Arial", 12))
        self.label.setFixedWidth(300)
        self.label.setStyleSheet("""
                    QLabel {
                        background-color: white;
                        border-radius: 10px;
                        padding: 10px;
                        font-size: 14px;
                    }
                """)

        layout.addWidget(self.label)

        # Force recalculation of label size based on word wrap
        self.label.adjustSize()
        self.adjustSize()

        self.label.adjustSize()
        self.adjustSize()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # Opacity effect
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        # Fade-in animation
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(500)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(0.5)
        self.fade_in.setEasingCurve(QEasingCurve.InOutQuad)

        # Fade-out animation
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(500)
        self.fade_out.setStartValue(0.5)
        self.fade_out.setEndValue(0)
        self.fade_out.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_out.finished.connect(self.close)

        # Trigger fade-out after timeout
        QTimer.singleShot(timeout, self.start_fade_out)

        self.key_timer = QTimer()
        self.key_timer.timeout.connect(self.check_key_press)
        self.key_timer.start(100)

    def start_fade_out(self):
        self.fade_out.start()

    def show_above_model_corner(self, model_widget):
        self.label.adjustSize()
        self.adjustSize()

        model_global_top_left = model_widget.mapToGlobal(QtCore.QPoint(0, 0))
        model_global_bottom_left = model_widget.mapToGlobal(QtCore.QPoint(0, model_widget.height()))

        # Place popup just below and aligned to model's left edge
        x = model_global_bottom_left.x()
        y = model_global_top_left.y() - self.height()

        self.move(x, max(y, 0))
        self.show()
        self.fade_in.start()

    def check_key_press(self):
        if keyboard.is_pressed(self.destroy_key):
            self.close_and_destroy()

    def close_and_destroy(self):
        self.close()
        self.deleteLater()
