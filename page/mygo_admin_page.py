
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QDialog,
    QFormLayout,
    QFrame,
    QLabel,
    QDialogButtonBox,
    QTableWidgetItem,
    QWidget
)


class Admin_Page(QWidget):
    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack
        self.db = db
        
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(18)

        header = QFrame()
        header.setObjectName("Card")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(22, 18, 22, 18)

        title = QLabel("Book Management")
        title.setObjectName("Title")
        subtitle = QLabel("Maintain books, manage users and view borrowing records")
        subtitle.setObjectName("Subtitle")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        search_bar = QFrame()
        search_bar.setObjectName("Card")
        search_layout = QHBoxLayout(search_bar)
        search_layout.setContentsMargins(16, 14, 16, 14)
        search_layout.setSpacing(12)

        return_btn = QPushButton("Exit Admin")
        return_btn.clicked.connect(self.return_homepage)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title or author")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search)
        change_btn = QPushButton("Switch to User Management")
        change_btn.clicked.connect(self.change_to_user_manage_page)
        search_layout.addWidget(return_btn)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(change_btn)

        body = QHBoxLayout()
        body.setSpacing(18)

        left_panel = QFrame()
        left_panel.setObjectName("Card")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(12)
        left_layout.addWidget(QLabel("Admin Actions"))

        lookup_borrow_book_btn = QPushButton("View Borrowed Books")
        lookup_borrow_book_btn.clicked.connect(self.go_borrowed_page)
        show_all_book_borrowed_log_btn = QPushButton("View All Borrowing Logs")
        show_all_book_borrowed_log_btn.clicked.connect(self.go_to_all_borrowed_page)
        add_book_btn = QPushButton("Add New Book")
        add_book_btn.clicked.connect(self.edit_new_book)
        edit_book_btn = QPushButton("Edit Book Info")
        edit_book_btn.clicked.connect(self.edit_book_information)
        left_layout.addWidget(lookup_borrow_book_btn)
        left_layout.addWidget(show_all_book_borrowed_log_btn)
        left_layout.addWidget(add_book_btn)
        left_layout.addWidget(edit_book_btn)
        left_layout.addStretch(1)

        table_wrap = QFrame()
        table_wrap.setObjectName("Card")
        table_layout = QVBoxLayout(table_wrap)
        table_layout.setContentsMargins(14, 14, 14, 14)
        table_layout.setSpacing(10)



        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "ISBN", "Status", "Action 1", "Action 2"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(44)
        table_layout.addWidget(self.table)

        body.addWidget(left_panel, 1)
        body.addWidget(table_wrap, 4)

        root.addWidget(header)
        root.addWidget(search_bar)
        root.addLayout(body, 1)
    
    def return_homepage(self):
        self.stack.setCurrentIndex(0)

    def change_to_user_manage_page(self):
        self.stack.setCurrentIndex(5)

    def borrow_book(self, book):
        book_id = book[0]
        user_id = self.stack.current_user["id"]
        
        if book[4] == "Borrowed":
            QMessageBox.warning(self, "Notice", "This book is already borrowed")
            return
        try:
            self.db.borrow_book(user_id, book_id)
            QMessageBox.information(self, "Success", f"'{book[1]}' borrowed successfully")
            self.load_books()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Borrowing failed: {e}")

    def delete_book(self, book):
        book_id = book[0]
        try:
            self.db.delete_book(book_id)
            QMessageBox.information(self, "Success", f"'{book[1]}' deleted successfully")
            self.load_books()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Deletion failed: {e}")


    def edit_new_book(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Book")

        form_layout = QFormLayout()

        title_input = QLineEdit()
        author_input = QLineEdit()
        isbn_input = QLineEdit()

        form_layout.addRow("Title", title_input)
        form_layout.addRow("Author", author_input)
        form_layout.addRow("ISBN", isbn_input)

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        main_edit_book_layout = QVBoxLayout()
        main_edit_book_layout.addLayout(form_layout)
        main_edit_book_layout.addLayout(btn_layout)
        dialog.setLayout(main_edit_book_layout)

        def save_book():
            title = title_input.text().strip()
            author = author_input.text().strip()
            isbn = isbn_input.text().strip()

            if not title or not author:
                QMessageBox.warning(dialog, "Notice", "Title and Author cannot be empty")
                return
            try:
                self.db.add_book(title, author, isbn if isbn else None)
                QMessageBox.information(dialog, "Success", "Book added successfully")
                dialog.accept()
                self.load_books()
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Failed to add: {e}")

        save_btn.clicked.connect(save_book)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()
        
    def go_borrowed_page(self):
        self.stack.setCurrentIndex(6)

    def go_to_all_borrowed_page(self):
        self.stack.setCurrentIndex(7)

    def edit_book_information(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Book")

        form_layout = QFormLayout()

        id_input = QLineEdit()
        title_input = QLineEdit()
        author_input = QLineEdit()
        isbn_input = QLineEdit()

        form_layout.addRow("ID to Edit", id_input)
        form_layout.addRow("New Title", title_input)
        form_layout.addRow("New Author", author_input)
        form_layout.addRow("New ISBN", isbn_input)

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        main_edit_book_layout = QVBoxLayout()
        main_edit_book_layout.addLayout(form_layout)
        main_edit_book_layout.addLayout(btn_layout)
        dialog.setLayout(main_edit_book_layout)

        def save_book():
            book_id = id_input.text().strip()
            title = title_input.text().strip()
            author = author_input.text().strip()
            isbn = isbn_input.text().strip()

            if not book_id:
                QMessageBox.warning(dialog, "Notice", "Book ID cannot be empty")
                return
            
            if not self.db.select_book_id_exist(book_id):
                QMessageBox.warning(dialog, "Notice", "Book ID does not exist")
                return

            if not title or not author:
                QMessageBox.warning(dialog, "Notice", "Title and Author cannot be empty")
                return
            try:
                self.db.update_book(book_id, title, author, isbn if isbn else None)
                QMessageBox.information(dialog, "Success", "Book updated successfully")
                dialog.accept()
                self.load_books()
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Update failed: {e}")

        save_btn.clicked.connect(save_book)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_books()

    def load_books(self):
        books = self.db.search_books("")
        self.populate_table(books)

    def search(self):
        keyword = self.search_input.text()
        books = self.db.search_books(keyword)
        self.populate_table(books)

    def populate_table(self, books):
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            for col, value in enumerate(book):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

            borrow_btn = QPushButton("Borrow")
            borrow_btn.clicked.connect(lambda checked, b=book: self.borrow_book(b))
            self.table.setCellWidget(row, 5, borrow_btn)

            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, b=book: self.delete_book(b))
            self.table.setCellWidget(row, 6, delete_btn)

