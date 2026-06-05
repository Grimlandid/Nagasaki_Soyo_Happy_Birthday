import os
import shutil
import sqlite3
import sys


def app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(app_dir(), "soyo_library_emm.db")

        self.db_path = db_path
        self._ensure_db_file()

        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def _ensure_db_file(self):
        if os.path.exists(self.db_path):
            return

        bundled_db = os.path.join(getattr(sys, '_MEIPASS', app_dir()), "soyo_library_emm.db")
        if os.path.exists(bundled_db):
            shutil.copy2(bundled_db, self.db_path)

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                status TEXT DEFAULT 'Available'
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'Reader'
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_id INTEGER,
                borrow_date TEXT,
                return_date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()

    def add_book(self, title, author, isbn):
        self.cursor.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (title, author, isbn))
        self.conn.commit()

    def add_user(self, username, password, role="Reader"):
        self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        self.conn.commit()

    def search_books(self, keyword):
        self.cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
        return self.cursor.fetchall()

    def search_users(self, keyword):
        self.cursor.execute("SELECT * FROM users WHERE username LIKE ?", (f"%{keyword}%",))
        return self.cursor.fetchall()

    def find_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()

    def borrow_book(self, user_id, book_id):
        self.cursor.execute("UPDATE books SET status = 'Borrowed' WHERE id = ? AND status = 'Available'", (book_id,))
        self.cursor.execute("INSERT INTO borrow_records (user_id, book_id, borrow_date) VALUES (?, ?, date('now'))", (user_id, book_id))
        self.conn.commit()

    def return_book(self, user_id, book_id):
        self.cursor.execute("UPDATE books SET status = 'Available' WHERE id = ?", (book_id,))
        self.cursor.execute("UPDATE borrow_records SET return_date = date('now') WHERE user_id = ? AND book_id = ? AND return_date IS NULL", (user_id, book_id))
        self.conn.commit()

    def get_borrowed_book_by_user(self, user_id):
        self.cursor.execute("""
            SELECT books.id, books.title, books.author, books.isbn, borrow_records.borrow_date FROM books
            JOIN borrow_records ON books.id = borrow_records.book_id
            WHERE borrow_records.user_id = ? AND borrow_records.return_date IS NULL
        """, (user_id,))
        return self.cursor.fetchall()

    def get_all_book_borrow_records(self):
        self.cursor.execute("""
            SELECT borrow_records.id, users.username, books.title, books.author, books.isbn, borrow_records.borrow_date, borrow_records.return_date FROM borrow_records
            JOIN books ON books.id = borrow_records.book_id
            JOIN users ON users.id = borrow_records.user_id
            ORDER BY borrow_records.id
        """)
        return self.cursor.fetchall()

    def delete_book(self, book_id):
        self.cursor.execute("""
            DELETE FROM books WHERE id = ?
        """, (book_id,))
        self.conn.commit()

    def update_book(self, book_id, title, author, isbn):
        self.cursor.execute("""
            UPDATE books SET title = ?, author = ?, isbn = ? WHERE id = ?
        """, (title, author, isbn, book_id))
        self.conn.commit()

    def select_book_id_exist(self, book_id):
        self.cursor.execute("""
            SELECT * FROM books WHERE id = ?
    """, (book_id,))
        return self.cursor.fetchone()

    def delete_user(self, user_id):
        self.cursor.execute("""
            DELETE FROM users WHERE id = ?
        """, (user_id,))
        self.conn.commit()

    def update_user(self, user_id, username, password):
        self.cursor.execute("""
            UPDATE users SET username = ?, password = ? WHERE id = ?
    """, (username, password, user_id))
        self.conn.commit()

    def change_user_role(self, username, role):
        self.cursor.execute("""
            UPDATE users SET role = ? WHERE username = ?
        """, (role, username))
        self.conn.commit()

    def add_any_user(self, username, password, role):
        self.cursor.execute("""
            INSERT INTO users (username, password, role) VALUES (?, ?, ?)
    """, (username, password, role))
        self.conn.commit()
