import os
import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

basedir = os.path.dirname("C:\\Users\\user\\Pictures\\")
print("Current working folder:", os.getcwd())
print("Paths are relative to:", basedir)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QLabel("GOOD DAY")
        widget.setPixmap(QPixmap(os.path.join(basedir, "아기 시추.png")))

        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()