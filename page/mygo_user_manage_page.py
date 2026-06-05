
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QDialog,
    QComboBox,
    QMessageBox,
    QLabel,
    QFrame,
    QTableWidgetItem,
    QWidget
)


class User_Manage_Page(QWidget):
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
        title = QLabel("User Management")
        title.setObjectName("Title")
        subtitle = QLabel("Search, Edit, Delete and Add users")
        subtitle.setObjectName("Subtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        search_bar = QFrame()
        search_bar.setObjectName("Card")
        search_layout = QHBoxLayout(search_bar)
        search_layout.setContentsMargins(16, 14, 16, 14)
        search_layout.setSpacing(12)

        return_btn = QPushButton("Back to Book Management")
        return_btn.clicked.connect(self.return_admin_page)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter username to search")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search)
        admin_add_user_btn = QPushButton("Add User")
        admin_add_user_btn.clicked.connect(self.admin_add_new_user)
        search_layout.addWidget(return_btn)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(admin_add_user_btn)

        table_wrap = QFrame()
        table_wrap.setObjectName("Card")
        table_layout = QVBoxLayout(table_wrap)
        table_layout.setContentsMargins(14, 14, 14, 14)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Password", "Role", "Action 1", "Action 2", "Action 3"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        table_layout.addWidget(self.table)

        root.addWidget(header)
        root.addWidget(search_bar)
        root.addWidget(table_wrap, 1)

    def return_admin_page(self):
        self.stack.setCurrentIndex(4)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_users()

    def load_users(self):
        users = self.db.search_users("")
        self.populate_table(users)

    def search(self):
        keyword = self.search_input.text()
        users = self.db.search_users(keyword)
        self.populate_table(users)

    def populate_table(self, users):
        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            new_role = "Promote" if user[3] == "Reader" else "Demote"
            for col, value in enumerate(user):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

            delete_user_btn = QPushButton("Delete")
            alert_user_btn = QPushButton("Edit")
            change_user_role_btn = QPushButton(new_role)
            delete_user_btn.clicked.connect(lambda checked, u=user: self.delete_user(u))
            alert_user_btn.clicked.connect(lambda checked, u=user: self.alert_user(u))
            change_user_role_btn.clicked.connect(lambda checked, u=user: self.change_user_role(u))
            self.table.setCellWidget(row, 4, delete_user_btn)
            self.table.setCellWidget(row, 5, alert_user_btn)
            self.table.setCellWidget(row, 6, change_user_role_btn)
            

    def delete_user(self, user):
        user_id = user[0]
        my_user_id = self.stack.current_user["id"]
        if not user_id == my_user_id:
            try:
                self.db.delete_user(user_id)
                QMessageBox.information(self, "Success", f"User '{user[1]}' deleted successfully")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Deletion failed: {e}")
        else:
            QMessageBox.critical(self, "Error", "You cannot delete your own account!")

    def alert_user(self, user):
        user_id = user[0]
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit User")

        form_layout = QFormLayout()

        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Username", username_input)
        form_layout.addRow("Password", password_input)

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        main_edit_user_layout = QVBoxLayout()
        main_edit_user_layout.addLayout(form_layout)
        main_edit_user_layout.addLayout(btn_layout)
        dialog.setLayout(main_edit_user_layout)

        def save_user():
            username = username_input.text().strip()
            password = password_input.text().strip()


            if not username or not password:
                QMessageBox.warning(dialog, "Notice", "Username and Password cannot be empty")
                return
            finduser = self.db.find_user(username)
            if not finduser is None and username != self.stack.current_user["username"]:
                QMessageBox.warning(dialog, "Notice", "Username already exists!")
                return
            try:
                self.db.update_user(user_id ,username, password)
                QMessageBox.information(dialog, "Success", "User updated successfully")
                dialog.accept()
                self.load_users()
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Update failed: {e}")

        save_btn.clicked.connect(save_user)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

    def change_user_role(self, user):
        dialog = QDialog(self)
        dialog.setWindowTitle("Warning!")
        
        username = user[1]
        if username == self.stack.current_user["username"]:
            QMessageBox.warning(dialog, "Error", "You cannot change your own role")
            return
        role = "Reader" if user[3] == "Admin" else "Admin"
        self.db.change_user_role(username, role)
        self.load_users()

    def admin_add_new_user(self):

        dialog = QDialog(self)
        dialog.setWindowTitle("Add New User")

        form_layout = QFormLayout()

        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        role_chose = QComboBox()

        role_chose.addItem("Reader")
        role_chose.addItem("Admin")

        form_layout.addRow("Username", username_input)
        form_layout.addRow("Password", password_input)
        form_layout.addRow("Role", role_chose)

        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        main_add_user_layout = QVBoxLayout()
        main_add_user_layout.addLayout(form_layout)
        main_add_user_layout.addLayout(btn_layout)
        dialog.setLayout(main_add_user_layout)

        def save_new_user():
            username = username_input.text().strip()
            password = password_input.text().strip()
            role = role_chose.currentText()

            if not username or not password:
                QMessageBox.warning(dialog, "Notice", "Username and Password cannot be empty")
                return
            finduser = self.db.find_user(username)
            if not finduser is None:
                QMessageBox.warning(dialog, "Notice", "Username already exists!")
                return
            try:
                self.db.add_any_user(username, password, role)
                QMessageBox.information(dialog, "Success", "User added successfully")
                dialog.accept()
                self.load_users()
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Failed to add: {e}")

        save_btn.clicked.connect(save_new_user)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

