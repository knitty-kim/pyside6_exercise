import os
import sys
import sqlite3

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTableWidgetItem,
    QTableWidget, QLineEdit, QWidget, QMessageBox
)
from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader

# base_dir = os.path.dirname(os.getcwd())
# print(base_dir)
# ui_file_path = os.path.join(base_dir, "ui_folder", "ui_account_manager.ui")
# print(ui_file_path)


# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def print_ui_objects(parent_widget):
    # 현재 UI 파일 내 객체를 출력
    print("UI 파일에 포함된 객체들:")
    for child in parent_widget.children():
        print(f" - {child.objectName()} ({child.__class__.__name__})")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_window = None
        self.edit_window = None
        self.load_ui()
        self.load_accounts()

    def load_ui(self):
        # QFile
        ui_file = QFile("ui_folder/ui_account_manager.ui")
        ### ui_file.open(QFile.ReadOnly)

        # QUiLoader
        loader = QUiLoader()
        loaded_ui = loader.load(ui_file, self)
        ui_file.close()

        self.setCentralWidget(loaded_ui)
        self.resize(loaded_ui.size())

        # print_ui_objects(loaded_ui)

        self.search_input = loaded_ui.findChild(QLineEdit, "searchInput")
        self.search_button = loaded_ui.findChild(QPushButton, "searchButton")
        self.search_button.clicked.connect(self.search_accounts)

        add_button = loaded_ui.findChild(QPushButton, "addButton")  # 버튼 ID
        add_button.clicked.connect(self.open_add_window)

        self.account_table = loaded_ui.findChild(QTableWidget, "accountTable")
        self.account_table.setHorizontalHeaderLabels(["플랫폼", "아이디", "비밀번호"])
        self.account_table.itemDoubleClicked.connect(self.open_edit_window)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            self.search_accounts()
        elif key == Qt.Key_Escape:
            # callback_func()
            pass

    # 모든 계정 로드
    def load_accounts(self):
        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT platform, username, password FROM accounts")
        rows = cursor.fetchall()
        conn.close()

        print("load_accounts 함수 호출됨!!")
        self.display_accounts(rows)

    # 계정 검색
    def search_accounts(self):
        search_term = self.search_input.text().strip()

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT platform, username, password FROM accounts WHERE platform LIKE ? OR username LIKE ?",
                       (f"%{search_term}%", f"%{search_term}%"))
        rows = cursor.fetchall()
        conn.close()

        self.display_accounts(rows)

    # 테이블에 계정 표시
    def display_accounts(self, accounts):
        self.account_table.setRowCount(len(accounts))
        for row_idx, account in enumerate(accounts):
            for col_idx, item in enumerate(account):
                self.account_table.setItem(row_idx, col_idx, QTableWidgetItem(item))

    def open_add_window(self):
        if not self.add_window:
            self.add_window = AddWindow()
        else:
            self.add_window.close()
        # self.add_window.destroyed.connect(self.load_accounts)
        self.add_window.show()


    def open_edit_window(self, item):
        row = item.row()
        # print(row)
        platform = self.account_table.item(row, 0).text()
        id = self.account_table.item(row, 1).text()
        password = self.account_table.item(row, 2).text()

        if not self.edit_window:
            self.edit_window = EditWindow(platform, id, password)
            self.edit_window.show()
        else:
            self.edit_window.close()
            self.edit_window = EditWindow(platform, id, password)
            self.edit_window.show()


class AddWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()

    def save(self):
        platform = self.platform_input.text().strip()
        id = self.id_input.text().strip()
        password = self.password_input.text().strip()

        if not platform or not id or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (platform, username, password) VALUES (?, ?, ?)",
                       (platform, id, password))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", f"Account for {platform} added successfully!")
        self.platform_input.clear()
        self.id_input.clear()
        self.password_input.clear()

        self.destroy()

    def load_ui(self):
        # QFile
        ui_file = QFile("ui_folder/ui_account_add.ui")

        # QUiLoader
        loader = QUiLoader()
        loaded_ui = loader.load(ui_file, self)
        ui_file.close()

        self.setCentralWidget(loaded_ui)
        self.resize(loaded_ui.size())

        self.platform_input = loaded_ui.findChild(QLineEdit, "lineEdit_platform")
        self.id_input = loaded_ui.findChild(QLineEdit, "lineEdit_id")
        self.password_input = loaded_ui.findChild(QLineEdit, "lineEdit_password")

        self.save_button = loaded_ui.findChild(QPushButton, "saveButton")
        self.save_button.clicked.connect(self.save)

        self.cancel_button = loaded_ui.findChild(QPushButton, "cancelButton")
        self.cancel_button.clicked.connect(self.close)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            self.save()
        elif key == Qt.Key_Escape:
            self.close()


class EditWindow(QMainWindow):
    def __init__(self, platform, id, password):
        super().__init__()
        self.load_ui(platform, id, password)

    def save(self):
        # QFile
        pass

    def load_ui(self, platform, id, password):
        # QFile
        ui_file = QFile("ui_folder/ui_account_add.ui")

        # QUiLoader
        loader = QUiLoader()
        loaded_ui = loader.load(ui_file, self)
        ui_file.close()

        self.setCentralWidget(loaded_ui)
        self.resize(loaded_ui.size())

        save_button = loaded_ui.findChild(QPushButton, "saveButton")
        save_button.clicked.connect(self.save)

        cancel_button = loaded_ui.findChild(QPushButton, "cancelButton")
        cancel_button.clicked.connect(self.close)

        # 계정 출력
        platform_label = loaded_ui.findChild(QLineEdit, "lineEdit_platform")
        platform_label.clear()
        platform_label.setText(platform)
        id_label = loaded_ui.findChild(QLineEdit, "lineEdit_id")
        id_label.clear()
        id_label.setText(id)
        password_label = loaded_ui.findChild(QLineEdit, "lineEdit_password")
        password_label.clear()
        password_label.setText(password)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            # self.search_accounts()
            pass
        elif key == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

