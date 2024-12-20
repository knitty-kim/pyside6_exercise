import sys
import bcrypt
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt, QSize
import sqlite3


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


# 메인 윈도우 클래스
class AccountManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("계정 관리 프로그램")


        self.setGeometry(200, 200, 800, 500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.init_ui()

    def init_ui(self):
        
        # 입력 폼
        form_layout = QHBoxLayout()

        self.platform_input = QLineEdit()
        self.platform_input.setPlaceholderText("Platform (e.g., Google)")
        form_layout.addWidget(QLabel("Platform:"))
        form_layout.addWidget(self.platform_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username/Email")
        form_layout.addWidget(QLabel("Username:"))
        form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(QLabel("Password:"))
        form_layout.addWidget(self.password_input)

        self.add_button = QPushButton("Add Account")
        self.add_button.clicked.connect(self.add_account)
        form_layout.addWidget(self.add_button)

        self.layout.addLayout(form_layout)

        # 검색 입력
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by platform or username")
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_accounts)
        search_layout.addWidget(self.search_button)

        self.layout.addLayout(search_layout)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Platform", "Username", "Password"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)

        # 삭제 및 수정 버튼
        action_layout = QHBoxLayout()

        self.delete_button = QPushButton("Delete Account")
        self.delete_button.clicked.connect(self.delete_account)
        action_layout.addWidget(self.delete_button)

        self.update_button = QPushButton("Update Account")
        self.update_button.clicked.connect(self.update_account)
        action_layout.addWidget(self.update_button)

        self.layout.addLayout(action_layout)

        # 초기 데이터 로드
        self.load_accounts()

    # 계정 추가
    def add_account(self):
        platform = self.platform_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not platform or not username or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        # 비밀번호 해싱
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (platform, username, password) VALUES (?, ?, ?)",
                       (platform, username, hashed_password.decode('utf-8')))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", f"Account for {platform} added successfully!")
        self.platform_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.load_accounts()

    # 계정 검색
    def search_accounts(self):
        search_term = self.search_input.text().strip()

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, platform, username, password FROM accounts WHERE platform LIKE ? OR username LIKE ?",
                       (f"%{search_term}%", f"%{search_term}%"))
        rows = cursor.fetchall()
        conn.close()

        self.display_accounts(rows)

    # 계정 삭제
    def delete_account(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a row to delete.")
            return

        account_id = self.table.item(current_row, 0).text()

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Account deleted successfully!")
        self.load_accounts()

    # 계정 수정
    def update_account(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a row to update.")
            return

        account_id = self.table.item(current_row, 0).text()
        new_platform = self.platform_input.text().strip()
        new_username = self.username_input.text().strip()
        new_password = self.password_input.text().strip()

        if not new_platform or not new_username or not new_password:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET platform = ?, username = ?, password = ? WHERE id = ?",
                       (new_platform, new_username, hashed_password.decode('utf-8'), account_id))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Account updated successfully!")
        self.load_accounts()

    # 테이블에 계정 표시
    def display_accounts(self, accounts):
        self.table.setRowCount(len(accounts))
        for row_idx, account in enumerate(accounts):
            for col_idx, item in enumerate(account):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    # 모든 계정 로드
    def load_accounts(self):
        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, platform, username, password FROM accounts")
        rows = cursor.fetchall()
        conn.close()

        self.display_accounts(rows)


# 메인 실행
if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)
    window = AccountManager()
    window.show()
    sys.exit(app.exec())
