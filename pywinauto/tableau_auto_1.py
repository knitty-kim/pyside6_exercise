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

# 계정 추가
def add_account():
    platform = input("Enter platform (e.g., Google, Facebook): ")
    username = input("Enter username/email: ")
    password = input("Enter password: ")

    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (platform, username, password) VALUES (?, ?, ?)",
                   (platform, username, password))
    conn.commit()
    conn.close()
    print(f"Account for {platform} added successfully!")

# 모든 계정 조회
def view_accounts():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, platform, username FROM accounts")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("\nStored Accounts:")
        for row in rows:
            print(f"ID: {row[0]}, Platform: {row[1]}, Username: {row[2]}")
    else:
        print("\nNo accounts found.")

# 특정 플랫폼 또는 사용자 검색
def search_accounts():
    search_term = input("Enter platform or username to search: ")
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, platform, username FROM accounts WHERE platform LIKE ? OR username LIKE ?",
                   (f"%{search_term}%", f"%{search_term}%"))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("\nSearch Results:")
        for row in rows:
            print(f"ID: {row[0]}, Platform: {row[1]}, Username: {row[2]}")
    else:
        print("\nNo matching accounts found.")

# 메인 메뉴
def main():
    init_db()
    while True:
        print("\nAccount Manager")
        print("1. Add Account")
        print("2. View All Accounts")
        print("3. Search Account")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_account()
        elif choice == "2":
            view_accounts()
        elif choice == "3":
            search_accounts()
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
