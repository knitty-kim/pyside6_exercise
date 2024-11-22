import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MY APP")

        button = QPushButton("CLICK!")

        self.setFixedSize(QSize(400, 300))
        self.setMinimumSize(QSize(300, 200))
        self.setMaximumSize(QSize(500, 400))

        self.setCentralWidget(button)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()