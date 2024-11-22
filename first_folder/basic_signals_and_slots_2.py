import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MY APP")

        self.button = QPushButton("PRESS ME!")

        # 신호
        # 이벤트가 발생했을 때, 위젯이 보내는 알림
        # 버튼 누르기, 텍스트 입력하기 등..
        # 신호는 이벤트에 대한 컨텍스트 데이터를 포함하기도 한다
        # 여기서는 clicked가 신호
        self.button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(self.button)

    # 슬롯 메서드
    # 버튼 클릭 이벤트와 연결된 메서드
    def the_button_was_clicked(self):
        self.button.setText("You already clicked")
        self.button.setEnabled(False)

        self.setWindowTitle("One shot APP")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()