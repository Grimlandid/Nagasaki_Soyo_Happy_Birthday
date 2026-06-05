import sys
from PyQt5.QtWidgets import (
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QApplication
)
from page.mygo_login_page import Login_Page
from page.mygo_register_page import Register_Page
from page.mygo_reader_page import Book_Manage_Page
from page.mygo_admin_page import Admin_Page
from page.mygo_user_manage_page import User_Manage_Page
from page.mygo_borrow_page import Borrowed_Page
from page.mygo_all_borrow_page import All_Borrow_Page
from page.soyo_library_homepage import Soyo_Library_Home_Page
from soyo_library_emm_db import Database


SOYO_LIBRARY_APP_STYLE = """
QWidget {
    font-family: "Microsoft YaHei";
    font-size: 13px;
    color: #2f2f2f;
    background-color: #f5f7fb;
}
QPushButton {
    background-color: #4f7cff;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 8px 16px;
    font-weight: 600;
}
QLabel#Title {
    font-size: 26px;
    font-weight: 700;
    color: #22304a;
}
QLabel#Subtitle {
    color: #667085;
    font-size: 12px;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #4f7cff;
}
QLineEdit {
    border-radius: 10px;
    border: 1px solid #d7deea;
}
QFrame#Card {
    background-color: white;
    border-radius: 10px;
}
QPushButton:hover {
    background-color: #3f6ff0;
}
QPushButton:pressed {
    background-color: #355fda;
}
QLineEdit, QComboBox {
    background-color: white;
    border: 1px solid #d7deea;
    border-radius: 10px;
    padding: 10px 12px;
    min-height: 18px;
}
QTableWidget {
    background: white;
    border: 1px solid #e6eaf2;
    border-radius: 14px;
    gridline-color: #eef1f6;
    alternate-background-color: #fafbfd;
}
QHeaderView::section {
    background-color: #eff4ff;
    color: #25324b;
    padding: 10px;
    border: none;
    border-bottom: 1px solid #dce5f5;
    font-weigth: 700;
}
"""


class Soyo_Library_App(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        
        self.setWindowTitle("Soyorin's Library")
        self.setFixedSize(1120, 720)
        self.setStyleSheet(SOYO_LIBRARY_APP_STYLE)

        self.stack = QStackedWidget()
        self.stack.current_user = None
        self.homepage = Soyo_Library_Home_Page(self.stack)
        self.login_page = Login_Page(self.stack, self.db, on_login_success=self.on_login_success)
        self.register_page = Register_Page(self.stack, self.db)
        self.book_manage_page = Book_Manage_Page(self.stack, self.db)
        self.admin_page = Admin_Page(self.stack, self.db)
        

        self.stack.addWidget(self.homepage)
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)
        self.stack.addWidget(self.book_manage_page)
        self.stack.addWidget(self.admin_page)
        
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

    def on_login_success(self, user_info):
        self.stack.current_user = user_info
        if not hasattr(self, 'borrowed_page') or self.borrowed_page is None:
            self.user_manage_page = User_Manage_Page(self.stack, self.db)
            self.stack.addWidget(self.user_manage_page)
            self.borrowed_page = Borrowed_Page(self.stack, self.db)
            self.stack.addWidget(self.borrowed_page)
            self.all_borrowed_page = All_Borrow_Page(self.stack, self.db)
            self.stack.addWidget(self.all_borrowed_page)

        if user_info["role"] == "Reader":
            self.stack.setCurrentIndex(3)
        elif user_info["role"] == "Admin":
            self.stack.setCurrentIndex(4)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Soyo_Library_App()
    window.show()
    sys.exit(app.exec_())


