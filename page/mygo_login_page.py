
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QWidget,
    QLabel,
    QFrame
)

class Login_Page(QWidget):
    def __init__(self, stack, db, on_login_success=None):
        super().__init__()
        self.stack = stack
        self.db = db

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(14)

        title = QLabel("Login")
        title.setObjectName("Title")
        subtitle = QLabel("Enter your library account")
        subtitle.setObjectName("Subtitle")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.on_login_success = on_login_success

        login_soyo_library = QPushButton("Login!")
        login_soyo_library.clicked.connect(self.just_login)

        return_btn = QPushButton("Back to Home")
        return_btn.clicked.connect(self.return_homepage)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(8)  
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(login_soyo_library)
        card_layout.addWidget(return_btn)

        wrapper = QVBoxLayout()
        wrapper.addStretch(1)
        wrapper.addWidget(card, 0)
        wrapper.addStretch(2)

        root.addLayout(wrapper)


    def just_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        row = self.db.find_user(username)

        if row is not None:
            if row[2] == password:
                user_info = {
                    "id": row[0],
                    "username": row[1],
                    "role": row[3]
                }
                if self.on_login_success:
                    self.on_login_success(user_info)
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password")
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")
            pass
        
    def return_homepage(self):
        self.stack.setCurrentIndex(0)

    def go_to_book_manage_page(self):
        self.stack.setCurrentIndex(3)

    def go_to_admin_page(self):
        self.stack.setCurrentIndex(4)

    


    





