import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True

        self.setWindowTitle('MY APP')

        # self로 button을 정의하는 이유
        # self를 붙이면 버튼 객체는 클래스의 인스턴스와 수명을 함께한다
        # 1. QPushButton 객체를 "클래스의 인스턴스 속성"으로 정의하기 위함
        # 2. 이 클래스의 다른 메서드(the_button..)에서도 button을
        #    접근할 수 있게 하기 위함
        self.button = QPushButton("CLICK ME!")
        self.button.setCheckable(True)
        self.button.released.connect(self.the_button_was_released)
        self.button.setChecked(self.button_is_checked)

        self.setCentralWidget(self.button)

    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()
        print(self.button_is_checked)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()