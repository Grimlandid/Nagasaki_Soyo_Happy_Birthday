
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
    QFrame,
    QLabel,
    QMessageBox
)

class Register_Page(QWidget):
    def __init__(self, stack, db):
        super().__init__()
        self.db = db
        self.stack = stack

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(14)

        title = QLabel("Register")
        title.setObjectName("Title")
        subtitle = QLabel("Create a new library account")
        subtitle.setObjectName("Subtitle")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.re_password_input = QLineEdit()
        self.re_password_input.setPlaceholderText("Confirm Password")
        self.re_password_input.setEchoMode(QLineEdit.Password)

        self.register_btn = QPushButton("Register!")
        self.register_btn.clicked.connect(self.register_user)

        self.return_btn = QPushButton("Back to Home")
        self.return_btn.clicked.connect(self.return_homepage)
        
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(8)  
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.re_password_input)
        card_layout.addWidget(self.register_btn)
        card_layout.addWidget(self.return_btn)
        
        wrapper = QVBoxLayout()
        wrapper.addStretch(1)
        wrapper.addWidget(card)
        wrapper.addStretch(2)

        root.addLayout(wrapper)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        row = self.db.find_user(username)

        if row is not None:
            QMessageBox.warning(self, "Error", "Username already exists")
        else:
            self.db.add_user(username, password)
            QMessageBox.information(self, "Success", "Registration successful!")

    def return_homepage(self):
        self.stack.setCurrentIndex(0)

