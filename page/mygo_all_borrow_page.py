from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
    QPushButton,
    QTableWidgetItem,
    QWidget,
    QFrame,
    QLabel,
)

class All_Borrow_Page(QWidget):
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
        title = QLabel("All Borrowing Records")
        title.setObjectName("Title")
        subtitle = QLabel("View the complete borrowing history in the system")
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
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "User", "Title", "Author", "ISBN", "Borrow Date", "Return Date"])
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
        self.stack.setCurrentIndex(4)


    def load_books(self):
        books = self.db.get_all_book_borrow_records()
        self.populate_table(books)

    def populate_table(self, books):
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            for col, value in enumerate(book):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))