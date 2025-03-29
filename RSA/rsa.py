from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QFileDialog, QMessageBox, QGroupBox,
                            QFrame, QDialog, QApplication)
from PyQt6.QtCore import Qt, pyqtSlot, QTimer
from PyQt6.QtGui import QFont, QIcon
from RSA import sign_file, check_sign
import os
import weakref

class RSAFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # Словарь для хранения таймеров
        self.timers = {}
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 0, 20, 20)
        main_layout.setSpacing(10)
        
        # Информационный блок
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_frame.setStyleSheet("""
            #infoFrame {
                background-color: #e7f5ff;
                border-radius: 8px;
                border: 1px solid #a5d8ff;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        
        info_title = QLabel("Алгоритм RSA")
        info_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #1864ab;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel("RSA — криптографический алгоритм с открытым ключом, основанный на вычислительной сложности задачи факторизации больших целых чисел.")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        main_layout.addWidget(info_frame)
        
        # Выбор файла
        file_group = QGroupBox("Выбор файла")
        file_layout = QHBoxLayout(file_group)
        
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Выберите файл для подписи или проверки...")
        self.file_path.setReadOnly(True)
        
        browse_button = QPushButton("Обзор")
        browse_button.setFixedWidth(100)
        browse_button.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_button)
        
        main_layout.addWidget(file_group)
        
        # Операции
        operations_group = QGroupBox("Операции")
        operations_layout = QVBoxLayout(operations_group)
        
        buttons_layout = QHBoxLayout()
        
        sign_button = QPushButton("Подписать файл")
        sign_button.clicked.connect(self.sign_file)
        
        verify_button = QPushButton("Проверить подпись")
        verify_button.clicked.connect(self.verify_signature)
        
        buttons_layout.addWidget(sign_button)
        buttons_layout.addWidget(verify_button)
        
        operations_layout.addLayout(buttons_layout)
        
        # Статус операции
        status_group = QGroupBox("Статус операции")
        status_layout = QVBoxLayout(status_group)
        status_layout.setContentsMargins(10, 10, 10, 10)
        
        self.status_label = QLabel("Готов к работе")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFixedHeight(60)
        self.status_label.setStyleSheet("""
            padding: 15px;
            border-radius: 6px;
            background-color: #f8f9fa;
            color: #6c757d;
            font-weight: bold;
            font-size: 14px;
            text-align: center;
        """)
        status_layout.addWidget(self.status_label)
        
        operations_layout.addWidget(status_group)
        
        main_layout.addWidget(operations_group)
        main_layout.addStretch()
    
    @pyqtSlot()
    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выбрать файл", "", "Все файлы (*)")
        if filename:
            self.file_path.setText(filename)
    
    def sign_file(self):
        if not self.file_path.text():
            self.status_label.setText("Ошибка: Файл не выбран")
            self.status_label.setStyleSheet("""
                padding: 15px;
                border-radius: 6px;
                background-color: #f8d7da;
                color: #721c24;
                font-weight: bold;
                font-size: 14px;
                text-align: center;
            """)
            return
        
        try:
            # Устанавливаем статус "Подпись формируется"
            self.status_label.setText("Подпись формируется...")
            self.status_label.setStyleSheet("""
                padding: 15px;
                border-radius: 6px;
                background-color: #fff3cd;
                color: #856404;
                font-weight: bold;
                font-size: 14px;
                text-align: center;
            """)
            # Обновляем интерфейс, чтобы статус отобразился немедленно
            QApplication.processEvents()
            
            # Выполняем подпись файла
            file_path = self.file_path.text()
            folder = sign_file.sign_file(file_path)
            
            # Обновляем статус
            self.status_label.setText("Файл успешно подписан")
            self.status_label.setStyleSheet("""
                padding: 15px;
                border-radius: 6px;
                background-color: #d4edda;
                color: #155724;
                font-weight: bold;
                font-size: 14px;
                text-align: center;
            """)
            
            # Показываем всплывающее окно с путем к папке
            folder_path = os.path.dirname(file_path) + '/' + folder
            self.show_folder_path_dialog(folder_path)
            
        except Exception as e:
            self.status_label.setText(f"Ошибка при подписи файла: {str(e)}")
            self.status_label.setStyleSheet("""
                padding: 15px;
                border-radius: 6px;
                background-color: #f8d7da;
                color: #721c24;
                font-weight: bold;
                font-size: 14px;
                text-align: center;
            """)
    
    def show_folder_path_dialog(self, folder_path):
        # Создаем диалоговое окно
        dialog = QDialog(self)
        dialog.setWindowTitle("Информация")
        dialog.setFixedSize(500, 200)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: #4361ee;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a56d4;
            }
        """)
        
        # Создаем компоненты диалога
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Информационное сообщение
        info_label = QLabel("Файл успешно подписан")
        info_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #155724;")
        layout.addWidget(info_label)
        
        # Путь к папке
        path_layout = QHBoxLayout()
        path_label = QLabel("Путь к папке:")
        path_layout.addWidget(path_label)
        
        path_value = QLineEdit(folder_path)
        path_value.setReadOnly(True)
        path_layout.addWidget(path_value)
        
        copy_button = QPushButton("Копировать")
        copy_button.setFixedWidth(120)
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(folder_path, copy_button))
        path_layout.addWidget(copy_button)
        
        layout.addLayout(path_layout)
        
        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        dialog.exec()
    
    def copy_to_clipboard(self, text, button):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        
        # Изменяем текст кнопки на короткое время
        original_text = button.text()
        button.setText("Скопировано!")
        
        # Если для этой кнопки уже есть таймер, останавливаем его
        button_id = id(button)
        if button_id in self.timers:
            self.timers[button_id].stop()
        
        # Создаем новый таймер
        timer = QTimer(self)
        timer.setSingleShot(True)
        
        # Используем weakref для предотвращения утечек памяти
        weak_button = weakref.ref(button)
        
        def restore_text():
            btn = weak_button()
            if btn is not None:
                btn.setText(original_text)
        
        timer.timeout.connect(restore_text)
        timer.start(1500)
        
        # Сохраняем таймер в словаре
        self.timers[button_id] = timer
    
    def verify_signature(self):
        if not self.file_path.text():
            self.status_label.setText("Ошибка: Файл не выбран")
            self.status_label.setStyleSheet("""
                padding: 15px;
                border-radius: 6px;
                background-color: #f8d7da;
                color: #721c24;
                font-weight: bold;
                font-size: 14px;
                text-align: center;
            """)
            return
        
        try:
            file_path = self.file_path.text()
            signature_path = file_path
            
            # Проверяем наличие файла подписи
            if not os.path.exists(signature_path):
                self.status_label.setText("Ошибка: Файл подписи не найден")
                self.status_label.setStyleSheet("""
                    padding: 15px;
                    border-radius: 6px;
                    background-color: #fff3cd;
                    color: #856404;
                    font-weight: bold;
                    font-size: 14px;
                    text-align: center;
                """)
                return
            
            # Устанавливаем статус "Подпись проверяется"
            self.status_label.setText("Подпись проверяется...")
            self.status_label.setStyleSheet("""
                padding: 15px;
                border-radius: 6px;
                background-color: #fff3cd;
                color: #856404;
                font-weight: bold;
                font-size: 14px;
                text-align: center;
            """)
            # Обновляем интерфейс, чтобы статус отобразился немедленно
            QApplication.processEvents()
            
            # Проверяем подпись
            result = check_sign.check_sign(file_path)
            
            if result == "Signature is valid.":
                self.status_label.setText("Подпись верна. Файл не был изменен.")
                self.status_label.setStyleSheet("""
                    padding: 15px;
                    border-radius: 6px;
                    background-color: #d4edda;
                    color: #155724;
                    font-weight: bold;
                    font-size: 14px;
                    text-align: center;
                """)
            else:
                self.status_label.setText("Подпись недействительна. Файл был изменен или подпись некорректна.")
                self.status_label.setStyleSheet("""
                    padding: 15px;
                    border-radius: 6px;
                    background-color: #fff3cd;
                    color: #856404;
                    font-weight: bold;
                    font-size: 14px;
                    text-align: center;
                """)
            
        except Exception as e:
            self.status_label.setText(f"Ошибка при проверке подписи: {str(e)}")
            self.status_label.setStyleSheet("""
                padding: 15px;
                border-radius: 6px;
                background-color: #f8d7da;
                color: #721c24;
                font-weight: bold;
                font-size: 14px;
                text-align: center;
            """)
    
    def closeEvent(self, event):
        # Очищаем все таймеры при закрытии
        for timer in self.timers.values():
            timer.stop()
        self.timers.clear()
        super().closeEvent(event)
