import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MY APP")

        widget = QLabel("HELLO")
        font = widget.font()
        font.setPointSize(10)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # widget.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()