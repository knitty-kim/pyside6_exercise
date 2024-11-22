import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from random import choice

window_titles = [
    "MY APP",
    "MY APP",
    "Still My APP",
    "Still My APP",
    "What on earth",
    "What on earth",
    "This is surprising",
    "This is surprising",
    "Something went wrong"
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.n_times_clicked = 0
        self.setWindowTitle("My App")

        self.button = QPushButton("Click me!")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.windowTitleChanged.connect(self.the_window_title_changed)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        print("Clicked")
        new_window_title = choice(window_titles)
        print("Setting title: %s" % new_window_title)
        self.setWindowTitle(new_window_title)

    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title())





