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

        button = QPushButton('CLICK!')
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked) # 버튼이 클릭되면 연결

        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        print("CLICKED!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()