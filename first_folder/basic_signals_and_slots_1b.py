import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('MY APP')

        button = QPushButton('CLICK ME!')
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)

        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        print('CLICKED!')

    # 두 번째  인자는  check Flag 값이 boolean으로 들어온다
    def the_button_was_toggled(self, check):
        print("Checked : " + str(check) + "\n")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()