from PyQt5.QtWidgets import QFrame, QLabel,QWidget, QFormLayout, QVBoxLayout, QDialog, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QHeaderView, QMessageBox, QTableWidgetItem



class Book_Manage_Page(QWidget):
    def __init__(self, stack, db):
        super().__init__()
        self.db = db
        self.stack = stack

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(18)

        header = QFrame()
        header.setObjectName("Card")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(22, 18, 22, 18)
        title = QLabel("Book Search")
        title.setObjectName("Title")
        subtitle = QLabel("Search books, check borrowing status and change password")
        subtitle.setObjectName("Subtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        search_bar = QFrame()
        search_bar.setObjectName("Card")
        search_bar_layout = QHBoxLayout(search_bar)
        search_bar_layout.setContentsMargins(16, 14, 16, 14)
        search_bar_layout.setSpacing(12)

        return_btn = QPushButton("Exit Search")
        return_btn.clicked.connect(self.return_homepage)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title or author")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search)
        search_bar_layout.addWidget(return_btn)
        search_bar_layout.addWidget(self.search_input, 1)
        search_bar_layout.addWidget(search_btn)

        body = QHBoxLayout()
        body.setSpacing(18)

        left_panel = QFrame()
        left_panel.setObjectName("Card")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(12)
        left_layout.addWidget(QLabel("Quick Actions"))
        lookup_borrow_book_btn = QPushButton("View Borrowed Books")
        lookup_borrow_book_btn.clicked.connect(self.go_borrowed_page)
        edit_password_btn = QPushButton("Change Password")
        edit_password_btn.clicked.connect(self.edit_password)
        left_layout.addWidget(lookup_borrow_book_btn)
        left_layout.addWidget(edit_password_btn)
        left_layout.addStretch(1)

        table_wrap = QFrame()
        table_wrap.setObjectName("Card")
        table_layout = QVBoxLayout(table_wrap)
        table_layout.setContentsMargins(14, 14, 14, 14)
        table_layout.setSpacing(18)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "ISBN", "Status", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(44)
        table_layout.addWidget(self.table)

        body.addLayout(left_layout, 1)
        body.addWidget(table_wrap, 4)

        root.addWidget(header)
        root.addWidget(search_bar)
        root.addLayout(body, 1)
        

    def return_homepage(self):
        self.stack.setCurrentIndex(0)

    def go_borrowed_page(self):
        self.stack.setCurrentIndex(6)

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
            
    def edit_password(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Change Password")

        form_layout = QFormLayout()

        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Password", password_input)

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        main_edit_password_layout = QVBoxLayout()
        main_edit_password_layout.addLayout(form_layout)
        main_edit_password_layout.addLayout(btn_layout)
        dialog.setLayout(main_edit_password_layout)

        def save_password():
            password = password_input.text().strip()
            user_id = self.stack.current_user["id"]
            username = self.stack.current_user["username"]
            if not password:
                QMessageBox.warning(dialog, "Notice", "Password cannot be empty")
                return
            try:
                self.db.update_user(user_id, username, password)
                QMessageBox.information(dialog, "Success", "Password updated successfully")
                dialog.accept()
                self.load_books()
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Update failed: {e}")

        save_btn.clicked.connect(save_password)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

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