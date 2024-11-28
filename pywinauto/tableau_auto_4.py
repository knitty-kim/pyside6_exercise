import os
import sys
import sqlite3

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTableWidgetItem,
    QTableWidget, QLineEdit, QWidget, QMessageBox
)
from PySide6.QtCore import QFile, Qt, Signal
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

        # 검색창
        self.search_input = loaded_ui.findChild(QLineEdit, "searchInput")
        
        # 검색 버튼
        self.search_button = loaded_ui.findChild(QPushButton, "searchButton")
        self.search_button.clicked.connect(self.search_accounts)

        # 추가 버튼
        add_button = loaded_ui.findChild(QPushButton, "addButton")
        add_button.clicked.connect(self.open_add_window)
        
        # 삭제 버튼
        delete_button = loaded_ui.findChild(QPushButton, "deleteButton")
        delete_button.clicked.connect(self.delete_account)

        # 계정 목록
        self.account_table = loaded_ui.findChild(QTableWidget, "accountTable")
        self.account_table.setHorizontalHeaderLabels(["플랫폼", "아이디", "비밀번호"])
        
        # 계정 수정 이벤트 - 더블 클릭
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

    # 계정 추가 창 생성
    def open_add_window(self):
        if not self.add_window:
            self.add_window = AddWindow()

            # 저장 완료 신호 연결
            self.add_window.saved.connect(self.load_accounts)
        else:
            self.add_window.close()
        self.add_window.show()

    # 계정 수정 창 생성
    def open_edit_window(self, item):
        row = item.row()
        platform = self.account_table.item(row, 0).text()
        id = self.account_table.item(row, 1).text()
        password = self.account_table.item(row, 2).text()

        if self.edit_window and self.edit_window.isVisible():
            # 기존 창을 업데이트
            self.edit_window.update_fields(platform, id, password)
            self.edit_window.raise_()
            self.edit_window.activateWindow()

        else:
            # 새 창 생성
            self.edit_window = EditWindow(platform, id, password)
            # 수정 후 새로고침 연결
            self.edit_window.updated.connect(self.load_accounts)
            self.edit_window.show()

    # 계정 삭제 기능
    def delete_account(self):
        # 선택된 행 가져오기
        selected_items = self.account_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "계정 선택 오류", "삭제할 계정을 선택해야 합니다.")
            return

        # 선택된 행의 데이터 추출
        row = self.account_table.currentRow()
        platform = self.account_table.item(row, 0).text()
        id = self.account_table.item(row, 1).text()
        password = self.account_table.item(row, 2).text()

        # 삭제 확인 메시지
        confirmation = QMessageBox.question(
            self, "확인",
            f"{platform} 플랫폼에 대한 계정 {id}을 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        # 삭제 확정
        if confirmation == QMessageBox.Yes:
            conn = sqlite3.connect("accounts.db")
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM accounts WHERE platform = ? AND username = ? AND password = ?",
                (platform, id, password)
            )
            conn.commit()
            conn.close()
            
            # 삭제 성공 메시지
            QMessageBox.information(self, "", f"계정 삭제 성공!")

            # 테이블 새로고침
            self.load_accounts()

            
class AddWindow(QMainWindow):
    # 저장 완료 신호 저장
    saved = Signal()

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

        # 저장 완료 신호 방출
        self.saved.emit()

        self.close()

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
    # 수정 완료 신호
    updated = Signal()

    def __init__(self, platform, id, password):
        super().__init__()
        
        # 기존 데이터 임시 저장
        self.original_platform = platform
        self.original_id = id
        self.original_password = password

        self.load_ui(platform, id, password)

    def update_fields(self, platform, id, password):
        self.platform_input.setText(platform)
        self.id_input.setText(id)
        self.password_input.setText(password)

    def save(self):
        # 입력된 데이터
        platform = self.platform_input.text().strip()
        username = self.id_input.text().strip()
        password = self.password_input.text().strip()

        # 필수 입력
        if not platform or not username or not password:
            QMessageBox.warning(self, "입력 오류", "모든 필드를 입력해야 합니다.")
            return

        # 데이터베이스 업데이트
        try:
            conn = sqlite3.connect("accounts.db")
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE accounts
                SET platform = ?, username = ?, password = ?
                WHERE platform = ? AND username = ? AND password = ?
                """,
                (platform, username, password,
                 self.original_platform, self.original_id, self.original_password)
            )
            conn.commit()

            # 업데이트 성공 여부 확인
            if cursor.rowcount == 0:
                QMessageBox.warning(self, "수정 실패", "데이터를 찾을 수 없습니다.")
            else:
                QMessageBox.information(self, "성공", "계정 정보가 성공적으로 수정되었습니다!")

                # 수정 완료 신호 방출
                self.updated.emit()

                self.close()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"수정 실패: {e}")

        finally:
            conn.close()

    def load_ui(self, platform, id, password):
        # QFile
        ui_file = QFile("ui_folder/ui_account_add.ui")

        # QUiLoader
        loader = QUiLoader()
        loaded_ui = loader.load(ui_file, self)
        ui_file.close()

        self.setCentralWidget(loaded_ui)
        self.resize(loaded_ui.size())
        
        # 저장 버튼 연결
        save_button = loaded_ui.findChild(QPushButton, "saveButton")
        save_button.clicked.connect(self.save)
        
        # 취소 버튼 연결
        cancel_button = loaded_ui.findChild(QPushButton, "cancelButton")
        cancel_button.clicked.connect(self.close)

        # 계정 출력
        self.platform_input = loaded_ui.findChild(QLineEdit, "lineEdit_platform")
        self.id_input = loaded_ui.findChild(QLineEdit, "lineEdit_id")
        self.password_input = loaded_ui.findChild(QLineEdit, "lineEdit_password")

        self.platform_input.setText(platform)
        self.id_input.setText(id)
        self.password_input.setText(password)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            self.save()
        elif key == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

