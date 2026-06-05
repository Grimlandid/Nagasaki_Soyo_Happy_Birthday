from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
    QPushButton,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
    QFrame,
    QLabel,
)



class Borrowed_Page(QWidget):
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
        title = QLabel("Current Borrowing")
        title.setObjectName("Title")
        subtitle = QLabel("View and return books you have borrowed")
        subtitle.setObjectName("Subtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        bar = QFrame()
        bar.setObjectName("Card")
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(16, 14, 16, 14)
        return_btn = QPushButton("Back")
        return_btn.clicked.connect(self.return_last_page)
        bar_layout.addWidget(return_btn)
        bar_layout.addStretch(1)

        table_wrap = QFrame()
        table_wrap.setObjectName("Card")
        table_layout = QVBoxLayout(table_wrap)
        table_layout.setContentsMargins(14, 14, 14, 14)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "ISBN", "Borrow Date", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(44)
        table_layout.addWidget(self.table)

        root.addWidget(header)
        root.addWidget(bar)
        root.addWidget(table_wrap, 1)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_books()

    def return_last_page(self):
        if self.stack.current_user["role"] == "Reader":
            self.stack.setCurrentIndex(3)
        elif self.stack.current_user["role"] == "Admin":
            self.stack.setCurrentIndex(4)
        

    def load_books(self):
        if self.stack.current_user is None:
            return
        books = self.db.get_borrowed_book_by_user(self.stack.current_user["id"])
        self.populate_table(books)

    def populate_table(self, books):
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            for col, value in enumerate(book):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

            return_book_btn = QPushButton("Return")
            return_book_btn.clicked.connect(lambda checked, b=book: self.return_book(b))
            self.table.setCellWidget(row, 5, return_book_btn)

    def return_book(self, book):
        book_id = book[0]
        user_id = self.stack.current_user["id"]

        try:
            self.db.return_book(user_id, book_id)
            QMessageBox.information(self, "Success", f"'{book[1]}' returned successfully")
            self.load_books()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Return failed: {e}")