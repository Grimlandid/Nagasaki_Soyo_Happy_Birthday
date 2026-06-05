
import os
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QFrame, QLabel, QVBoxLayout, QPushButton, QMessageBox



def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)


class Soyo_Library_Home_Page(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("Soyo's Library")
        self.setGeometry(100, 100, 800, 600)

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.addSpacing(20)

        hero = QFrame()
        hero.setObjectName("Card")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(24, 24, 24, 24)
        hero_layout.setSpacing(20)

        login_btn = QPushButton("Login")
        register_btn = QPushButton("Register")

        login_btn.clicked.connect(self.go_to_login_page)
        register_btn.clicked.connect(self.go_to_register_page)

        title = QLabel("Welcome to Library Management System")
        title.setObjectName("Title")
        subtitle = QLabel("Read, Borrow, Manage, One-stop Library Service \t\t----Owner: Nagasaki Soyo")
        subtitle.setObjectName("Subtitle")

        left = QVBoxLayout(self)
        left.addStretch(1)
        left.addWidget(title)
        left.addWidget(subtitle)
        left.addSpacing(12)
        left.addWidget(login_btn)
        left.addWidget(register_btn)
        left.addStretch(1)

        right = QLabel()
        right.setMinimumSize(420, 420)
        right.setStyleSheet("border-radius: 14px; background-color: #f3f6ff;")
        right.setAlignment(Qt.AlignCenter)
        image = QPixmap(resource_path(r"image/Nagasaki_Soyo.jpg"))
        right.setPixmap(image.scaled(420, 420, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        hero_layout.addLayout(left, 1)
        hero_layout.addWidget(right, 1)

        root.addWidget(hero, 1)

    def go_to_login_page(self):
        self.stack.setCurrentIndex(1)

    def go_to_register_page(self):
        self.stack.setCurrentIndex(2)
