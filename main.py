import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QFrame, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QLinearGradient, QColor, QPalette
import RSA.rsa as rsa
import GOST.gost as gost

class SignatureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Цифровая Подпись")
        self.setGeometry(100, 100, 600, 600)
        
        # Set application-wide stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QPushButton {
                background-color: #4361ee;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a56d4;
            }
            QPushButton:pressed {
                background-color: #2a46c4;
            }
            QLabel {
                font-size: 14px;
                color: #212529;
            }
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e9ecef;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin-top: 14px;
                padding-top: 12px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #495057;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 10px;
                background-color: #ffffff;
                selection-background-color: #4361ee;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #4361ee;
                outline: none;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f1f3f5;
                border: 1px solid #dee2e6;
                border-bottom-color: #dee2e6;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                min-width: 10ex;
                padding: 10px 16px;
                margin-right: 2px;
                color: #495057;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
                color: #212529;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #e9ecef;
            }
            QComboBox {
                border: 1px solid #ced4da;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                min-width: 100px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #ced4da;
            }
            QScrollBar:vertical {
                border: none;
                background: #f8f9fa;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #adb5bd;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f8f9fa;
                height: 10px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #adb5bd;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(18)
        
        # Создаем кнопку назад
        self.back_button = QPushButton("← Назад")
        self.back_button.setObjectName("backButton")
        self.back_button.setFixedWidth(120)
        self.back_button.setStyleSheet("""
            #backButton {
                background-color: #6c757d;
                font-size: 13px;
            }
            #backButton:hover {
                background-color: #5a6268;
            }
        """)
        self.back_button.clicked.connect(self.show_main_menu)
        
        # Добавляем кнопку назад в отдельный контейнер
        back_container = QHBoxLayout()
        back_container.setContentsMargins(0, 0, 0, 10)
        back_container.addWidget(self.back_button)
        back_container.addStretch()
        self.main_layout.addLayout(back_container)
        
        self.back_button.hide()  # Hide initially
        
        # Content frame
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        self.content_frame.setStyleSheet("""
            #contentFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(18)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.content_frame)
        
        # Show main menu
        self.show_main_menu()
    
    def clear_content(self):
        # Clear all widgets from content layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def show_main_menu(self):
        self.clear_content()
        self.back_button.hide()
        
        # Create buttons with modern styling
        rsa_button = QPushButton("Цифровая подпись RSA")
        rsa_button.setObjectName("rsaButton")
        rsa_button.setFixedWidth(320)
        rsa_button.setMinimumHeight(70)
        rsa_button.setStyleSheet("""
            #rsaButton {
                background-color: #4361ee;
                font-size: 15px;
                border-radius: 8px;
            }
        """)
        rsa_button.clicked.connect(self.show_rsa_frame)
        
        gost_button = QPushButton("Цифровая подпись ГОСТ")
        gost_button.setObjectName("gostButton")
        gost_button.setFixedWidth(320)
        gost_button.setMinimumHeight(70)
        gost_button.setStyleSheet("""
            #gostButton {
                background-color: #3a0ca3;
                font-size: 15px;
                border-radius: 8px;
            }
        """)
        gost_button.clicked.connect(self.show_gost_frame)
        
        exit_button = QPushButton("Выход")
        exit_button.setObjectName("exitButton")
        exit_button.setFixedWidth(320)
        exit_button.setMinimumHeight(70)
        exit_button.setStyleSheet("""
            #exitButton {
                background-color: #e63946;
                font-size: 15px;
                border-radius: 8px;
            }
            #exitButton:hover {
                background-color: #d62b39;
            }
        """)
        exit_button.clicked.connect(self.close)
        
        # Logo or title - используем HTML для гарантированного размера
        app_title = QLabel()
        app_title.setText("<html><head/><body><p align='center'><span style='font-size:20pt; font-weight:600;'>Система цифровой подписи</span></p></body></html>")
        app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        app_subtitle = QLabel()
        app_subtitle.setText("<html><head/><body><p align='center'><span style='font-size:12pt; color:#6c757d;'>Защита и проверка целостности ваших данных</span></p></body></html>")
        app_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add buttons to layout with spacing
        self.content_layout.addStretch()
        self.content_layout.addWidget(app_title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addSpacing(10)
        self.content_layout.addWidget(app_subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addSpacing(50)
        self.content_layout.addWidget(rsa_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addSpacing(15)
        self.content_layout.addWidget(gost_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addSpacing(15)
        self.content_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addStretch()
    
    def show_rsa_frame(self):
        self.clear_content()
        self.back_button.show()
        
        # Create RSA frame
        rsa_frame = rsa.RSAFrame()
        self.content_layout.addWidget(rsa_frame)
    
    def show_gost_frame(self):
        self.clear_content()
        self.back_button.show()
        
        # Create GOST frame
        gost_frame = gost.GOSTFrame()
        self.content_layout.addWidget(gost_frame)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for a modern look
    window = SignatureApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
