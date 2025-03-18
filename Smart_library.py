import sqlite3
from datetime import datetime, timedelta

# Database setup
def initialize_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            user TEXT,
            borrow_date TEXT,
            due_date TEXT,
            return_date TEXT,
            fine INTEGER DEFAULT 0,
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    """)
    conn.commit()
    conn.close()

def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    book_id=input("Enter Book ID :")
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()
    print(f"Book '{title}' by {author} added successfully.")

def borrow_book():
    book_id = int(input("Enter book ID to borrow: "))
    user = input("Enter your name: ")
    days = int(input("Enter number of days to borrow (default 14): ") or 14)
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    cursor.execute("INSERT INTO transactions (book_id, user, borrow_date, due_date) VALUES (?, ?, ?, ?)", (book_id, user, borrow_date, due_date))
    conn.commit()
    conn.close()
    print(f"Book ID {book_id} borrowed by {user}, due on {due_date}.")

def return_book():
    book_id = int(input("Enter book ID to return: "))
    user = input("Enter your name: ")
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT due_date FROM transactions WHERE book_id = ? AND user = ? AND return_date IS NULL", (book_id, user))
    row = cursor.fetchone()
    if not row:
        print("No active borrow record found.")
        return
    due_date = datetime.strptime(row[0], '%Y-%m-%d')
    return_date = datetime.now()
    fine = max(0, (return_date - due_date).days * 10)  # Fine of $10 per overdue day
    cursor.execute("UPDATE transactions SET return_date = ?, fine = ? WHERE book_id = ? AND user = ? AND return_date IS NULL", (return_date.strftime('%Y-%m-%d'), fine, book_id, user))
    conn.commit()
    conn.close()
    print(f"Book ID {book_id} returned by {user}. Fine: ${fine}")

def generate_monthly_report():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    month = datetime.now().strftime('%Y-%m')
    cursor.execute("SELECT user, COUNT(*) FROM transactions WHERE borrow_date LIKE ? GROUP BY user", (f"{month}%",))
    report = cursor.fetchall()
    conn.close()
    print("\nMonthly Library Report:")
    for user, count in report:
        print(f"User: {user}, Books Borrowed: {count}")

def main():
    initialize_db()
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. Generate Monthly Report")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_book()
        elif choice == "2":
            borrow_book()
        elif choice == "3":
            return_book()
        elif choice == "4":
            generate_monthly_report()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()