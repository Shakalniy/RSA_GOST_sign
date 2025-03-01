from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QFileDialog, QMessageBox, QGroupBox,
                             QTabWidget, QTextEdit, QComboBox, QScrollArea, QFrame,
                             QRadioButton, QStackedWidget, QDialog, QApplication)
from PyQt6.QtCore import Qt, pyqtSlot, QTimer
from PyQt6.QtGui import QFont, QIcon
from GOST import sign_file, check_sign, stribog
import os
import sys

# Добавляем импорт констант
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants import sign_params_constants

class GOSTFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 0, 10, 10)  
        main_layout.setSpacing(5)  
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("gostTabWidget")
        self.tab_widget.setStyleSheet("""
            #gostTabWidget::pane {
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
                padding: 8px 16px;  
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
        """)
        
        # Create signature tab
        signature_tab = QWidget()
        self.setup_signature_tab(signature_tab)
        self.tab_widget.addTab(signature_tab, "Цифровая подпись")
        
        # Create hash tab
        hash_tab = QWidget()
        self.init_hash_tab(hash_tab)
        self.tab_widget.addTab(hash_tab, "Хеширование")
        
        main_layout.addWidget(self.tab_widget)
    
    def setup_signature_tab(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(20, 10, 20, 20)  
        layout.setSpacing(10)  
        
        # Информационный блок
        info_frame = QFrame()
        info_frame.setObjectName("infoFrameSignature")
        info_frame.setStyleSheet("""
            #infoFrameSignature {
                background-color: #ebfbee;
                border-radius: 8px;
                border: 1px solid #b2f2bb;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        
        info_title = QLabel("Алгоритм ГОСТ Р 34.10-2018")
        info_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #2b8a3e;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel("ГОСТ Р 34.10-2018 — российский стандарт электронной подписи, основанный на эллиптических кривых.")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_frame)
        
        # Выбор файла
        file_group = QGroupBox("Выбор файла")
        file_layout = QHBoxLayout(file_group)
        
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("Путь к файлу...")
        
        browse_button = QPushButton("Обзор")
        browse_button.setFixedWidth(100)
        browse_button.setStyleSheet("""
            background-color: #40c057;
            color: white;
            border-radius: 6px;
            font-weight: bold;
        """)
        browse_button.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(browse_button)
        
        layout.addWidget(file_group)
        
        # Выбор параметров
        params_group = QGroupBox("Параметры подписи")
        params_layout = QVBoxLayout(params_group)
        
        # Радиокнопки для выбора типа параметров
        self.gen_params_radio = QRadioButton("Генерировать параметры с нуля")
        self.use_constants_radio = QRadioButton("Использовать готовые параметры")
        self.gen_params_radio.setChecked(True)  # По умолчанию генерируем параметры
        
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.gen_params_radio)
        radio_layout.addWidget(self.use_constants_radio)
        radio_layout.addStretch()
        params_layout.addLayout(radio_layout)
        
        # Стек виджетов для выбора размера хеш-функции (только для готовых параметров)
        self.params_stack = QStackedWidget()
        
        # Пустой виджет для случая генерации параметров
        empty_widget = QWidget()
        
        # Виджет для выбора размера хеш-функции
        hash_size_widget = QWidget()
        hash_size_layout = QVBoxLayout(hash_size_widget)
        hash_size_layout.setContentsMargins(0, 10, 0, 0)
        
        hash_size_label = QLabel("Выберите размер хеш-функции:")
        hash_size_layout.addWidget(hash_size_label)
        
        # Радиокнопки для выбора размера хеша
        self.hash_256_radio_sign = QRadioButton("256 бит")
        self.hash_512_radio_sign = QRadioButton("512 бит")
        self.hash_256_radio_sign.setChecked(True)  # По умолчанию выбран размер 256 бит
        
        hash_size_radio_layout = QHBoxLayout()
        hash_size_radio_layout.addWidget(self.hash_256_radio_sign)
        hash_size_radio_layout.addWidget(self.hash_512_radio_sign)
        hash_size_radio_layout.addStretch()
        hash_size_layout.addLayout(hash_size_radio_layout)
        
        # Добавляем виджеты в стек
        self.params_stack.addWidget(empty_widget)
        self.params_stack.addWidget(hash_size_widget)
        
        # Подключаем сигналы радиокнопок к переключению стека
        self.gen_params_radio.toggled.connect(lambda checked: self.params_stack.setCurrentIndex(0) if checked else None)
        self.use_constants_radio.toggled.connect(lambda checked: self.params_stack.setCurrentIndex(1) if checked else None)
        
        params_layout.addWidget(self.params_stack)
        layout.addWidget(params_group)
        
        # Операции
        operations_group = QGroupBox("Операции")
        operations_layout = QVBoxLayout(operations_group)
        
        buttons_layout = QHBoxLayout()
        
        sign_button = QPushButton("Подписать файл")
        sign_button.setStyleSheet("""
            background-color: #40c057;
            color: white;
            border-radius: 6px;
            font-weight: bold;
            padding: 10px;
        """)
        sign_button.clicked.connect(self.sign_file)
        
        check_button = QPushButton("Проверить подпись")
        check_button.setStyleSheet("""
            background-color: #40c057;
            color: white;
            border-radius: 6px;
            font-weight: bold;
            padding: 10px;
        """)
        check_button.clicked.connect(self.check_signature)
        
        buttons_layout.addWidget(sign_button)
        buttons_layout.addWidget(check_button)
        
        operations_layout.addLayout(buttons_layout)
        
        # Статус операции
        status_group = QGroupBox("Статус операции")
        status_layout = QVBoxLayout(status_group)
        status_layout.setContentsMargins(10, 10, 10, 10)  
        
        self.status_label = QLabel("Готов к работе")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFixedHeight(60)  
        self.status_label.setStyleSheet("""
            padding: 10px;
            border-radius: 6px;
            background-color: #e9ecef;
            color: #495057;
            font-size: 14px;
            font-weight: bold;
            margin: 5px;
            text-align: center;
        """)
        
        status_layout.addWidget(self.status_label)
        
        operations_layout.addWidget(status_group)
        
        layout.addWidget(operations_group)
        layout.addStretch()
    
    def init_hash_tab(self, parent):
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
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
        
        info_title = QLabel("Алгоритм ГОСТ Р 34.11-2018")
        info_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #1864ab;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel("ГОСТ Р 34.11-2018 — современный российский криптографический стандарт, определяющий алгоритм вычисления хеш-функции Стрибог с длиной выхода 256 или 512 бит.")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_frame)
        
        # Выбор источника данных
        source_group = QGroupBox("Источник данных")
        source_layout = QVBoxLayout(source_group)
        
        # Радиокнопки для выбора источника
        self.file_radio = QRadioButton("Файл")
        self.text_radio = QRadioButton("Текст")
        self.file_radio.setChecked(True)  # По умолчанию выбран файл
        
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.file_radio)
        radio_layout.addWidget(self.text_radio)
        radio_layout.addStretch()
        source_layout.addLayout(radio_layout)
        
        # Стек виджетов для переключения между файлом и текстом
        self.source_stack = QStackedWidget()
        
        # Виджет для выбора файла
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(0, 10, 0, 0)
        
        self.hash_file_path = QLineEdit()
        self.hash_file_path.setPlaceholderText("Выберите файл для хеширования...")
        self.hash_file_path.setReadOnly(True)
        
        browse_button = QPushButton("Обзор")
        browse_button.setFixedWidth(100)
        browse_button.clicked.connect(self.browse_hash_file)
        
        file_layout.addWidget(self.hash_file_path)
        file_layout.addWidget(browse_button)
        
        # Виджет для ввода текста
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 10, 0, 0)
        
        self.hash_text_input = QTextEdit()
        self.hash_text_input.setPlaceholderText("Введите текст для хеширования...")
        self.hash_text_input.setMinimumHeight(100)
        
        text_layout.addWidget(self.hash_text_input)
        
        # Добавляем виджеты в стек
        self.source_stack.addWidget(file_widget)
        self.source_stack.addWidget(text_widget)
        
        # Подключаем сигналы радиокнопок к переключению стека
        self.file_radio.toggled.connect(lambda checked: self.source_stack.setCurrentIndex(0) if checked else None)
        self.text_radio.toggled.connect(lambda checked: self.source_stack.setCurrentIndex(1) if checked else None)
        
        source_layout.addWidget(self.source_stack)
        layout.addWidget(source_group)
        
        # Выбор размера хеш-функции
        hash_size_group = QGroupBox("Размер хеш-функции")
        hash_size_layout = QVBoxLayout(hash_size_group)
        
        # Радиокнопки для выбора размера хеша
        self.hash_256_radio = QRadioButton("256 бит")
        self.hash_512_radio = QRadioButton("512 бит")
        self.hash_256_radio.setChecked(True)  # По умолчанию выбран размер 256 бит
        
        hash_size_radio_layout = QHBoxLayout()
        hash_size_radio_layout.addWidget(self.hash_256_radio)
        hash_size_radio_layout.addWidget(self.hash_512_radio)
        hash_size_radio_layout.addStretch()
        hash_size_layout.addLayout(hash_size_radio_layout)
        
        layout.addWidget(hash_size_group)
        
        # Операции
        operations_group = QGroupBox("Операции")
        operations_layout = QVBoxLayout(operations_group)
        
        hash_button = QPushButton("Вычислить хеш")
        hash_button.clicked.connect(self.calculate_hash)
        operations_layout.addWidget(hash_button)
        
        layout.addWidget(operations_group)
        
        layout.addStretch()
        return parent
    
    @pyqtSlot()
    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выбрать файл", "", "Все файлы (*)")
        if filename:
            self.file_path_input.setText(filename)
    
    @pyqtSlot()
    def sign_file(self):
        file_path = self.file_path_input.text()
        if not file_path:
            self.status_label.setText("Ошибка: Файл не выбран")
            self.status_label.setStyleSheet("""
                padding: 10px;
                border-radius: 6px;
                background-color: #f8d7da;
                color: #721c24;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
                text-align: center;
            """)
            return
        
        try:
            # Устанавливаем статус "Подпись формируется"
            self.status_label.setText("Подпись формируется...")
            self.status_label.setStyleSheet("""
                padding: 10px;
                border-radius: 6px;
                background-color: #fff3cd;
                color: #856404;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
                text-align: center;
            """)
            # Обновляем интерфейс, чтобы статус отобразился немедленно
            QApplication.processEvents()
            
            # Выполняем подпись файла
            if self.use_constants_radio.isChecked():
                hash_size = 256 if self.hash_256_radio_sign.isChecked() else 512
                sign_file.sign_file(file_path, hash_size, sign_params_constants)
            else:
                sign_file.sign_file(file_path)
            
            # Обновляем статус
            self.status_label.setText("Файл успешно подписан")
            self.status_label.setStyleSheet("""
                padding: 10px;
                border-radius: 6px;
                background-color: #d4edda;
                color: #155724;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
                text-align: center;
            """)
            
            # Показываем всплывающее окно с путем к папке
            folder_path = os.path.dirname(file_path)
            self.show_folder_path_dialog(folder_path)
            
        except Exception as e:
            error_message = str(e)
            self.status_label.setText(f"Ошибка подписи файла: {error_message}")
            self.status_label.setStyleSheet("""
                padding: 10px;
                border-radius: 6px;
                background-color: #f8d7da;
                color: #721c24;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
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
                background-color: #2b8a3e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #237032;
            }
            QPushButton#copyButton {
                background-color: #20c997;
            }
            QPushButton#copyButton:hover {
                background-color: #12b886;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                font-family: monospace;
            }
        """)
        
        # Создаем компоненты диалога
        layout = QVBoxLayout(dialog)
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
        copy_button.clicked.connect(lambda: self.copy_folder_to_clipboard(folder_path, copy_button))
        path_layout.addWidget(copy_button)
        
        layout.addLayout(path_layout)
        
        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        dialog.exec()
    
    def copy_folder_to_clipboard(self, text, button):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        
        # Изменяем текст кнопки на короткое время
        original_text = button.text()
        button.setText("Скопировано!")
        
        # Возвращаем исходный текст через 1.5 секунды
        QTimer.singleShot(1500, lambda: button.setText(original_text))
    
    @pyqtSlot()
    def check_signature(self):
        file_path = self.file_path_input.text()
        if not file_path:
            self.status_label.setText("Ошибка: Файл не выбран")
            self.status_label.setStyleSheet("""
                padding: 10px;
                border-radius: 6px;
                background-color: #f8d7da;
                color: #721c24;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
                text-align: center;
            """)
            return
        
        try:
            # Устанавливаем статус "Подпись проверяется"
            self.status_label.setText("Подпись проверяется...")
            self.status_label.setStyleSheet("""
                padding: 10px;
                border-radius: 6px;
                background-color: #fff3cd;
                color: #856404;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
                text-align: center;
            """)
            # Обновляем интерфейс, чтобы статус отобразился немедленно
            QApplication.processEvents()
            
            # Проверяем подпись
            if self.use_constants_radio.isChecked():
                hash_size = 256 if self.hash_256_radio_sign.isChecked() else 512
                result = check_sign.check_sign(file_path, hash_size)
            else:
                result = check_sign.check_sign(file_path)
            
            if result == "Signature is valid":
                result_text = "Подпись верна. Файл не был изменен."
            elif result == "Signature not found":
                result_text = "Подпись не найдена"
            else:
                result_text = "Подпись недействительна. Файл был изменен или подпись некорректна."
                
            self.status_label.setText(result_text)
            
            if result_text.startswith("Подпись верна"):
                self.status_label.setStyleSheet("""
                    padding: 10px;
                    border-radius: 6px;
                    background-color: #d4edda;
                    color: #155724;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 5px;
                    text-align: center;
                """)
            elif result_text == "Подпись не найдена":
                self.status_label.setStyleSheet("""
                    padding: 10px;
                    border-radius: 6px;
                    background-color: #fff3cd;
                    color: #856404;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 5px;
                    text-align: center;
                """)
            else:
                self.status_label.setStyleSheet("""
                    padding: 10px;
                    border-radius: 6px;
                    background-color: #fff3cd;
                    color: #856404;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 5px;
                    text-align: center;
                """)
        except Exception as e:
            error_message = str(e)
            self.status_label.setText(f"Ошибка проверки подписи: {error_message}")
            self.status_label.setStyleSheet("""
                padding: 10px;
                border-radius: 6px;
                background-color: #f8d7da;
                color: #721c24;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
                text-align: center;
            """)
    
    @pyqtSlot()
    def browse_hash_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выбрать файл", "", "Все файлы (*)")
        if filename:
            self.hash_file_path.setText(filename)
    
    @pyqtSlot()
    def calculate_hash(self):
        try:
            from GOST import stribog
            
            # Определяем размер хеш-функции
            hash_size = 256 if self.hash_256_radio.isChecked() else 512
            
            if self.file_radio.isChecked():
                # Хеширование файла
                file_path = self.hash_file_path.text()
                if not file_path:
                    self.show_warning_dialog("Файл не выбран", "Пожалуйста, выберите файл для хеширования.")
                    return
                
                hash_value = stribog.start_stribog(file_path, hash_size)
                source_type = "файла"
                source_name = file_path
            else:
                # Хеширование текста
                text = self.hash_text_input.toPlainText()
                if not text:
                    self.show_warning_dialog("Текст не введен", "Пожалуйста, введите текст для хеширования.")
                    return
                
                hash_value = stribog.start_stribog(text, hash_size)
                source_type = "текста"
                source_name = text[:30] + "..." if len(text) > 30 else text
            
            # Создаем всплывающее окно с результатом
            self.show_hash_result_dialog(hash_value, source_type, source_name, hash_size)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при хешировании: {str(e)}")
    
    def show_warning_dialog(self, title, message):
        # Создаем диалоговое окно предупреждения
        dialog = QDialog(self)
        dialog.setWindowTitle("Предупреждение")
        dialog.setFixedSize(400, 200)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #fff9db;
                border: 1px solid #ffe066;
                border-radius: 8px;
            }
            QLabel {
                color: #664d03;
                font-size: 14px;
            }
            QPushButton {
                background-color: #ffd43b;
                color: #664d03;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fcc419;
            }
        """)
        
        # Создаем компоненты диалога
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Иконка предупреждения
        icon_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        icon_label.setStyleSheet("""
            background-color: #ffd43b;
            border-radius: 24px;
            color: #664d03;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
        """)
        icon_label.setText("!")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(icon_layout)
        
        # Заголовок
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Сообщение
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message_label)
        
        # Кнопка OK
        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(100)
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        dialog.exec()
    
    def show_hash_result_dialog(self, hash_value, source_type, source_name, hash_size):
        # Создаем диалоговое окно
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Результат хеширования (ГОСТ Р 34.11-2018, {hash_size} бит)")
        dialog.setMinimumWidth(500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #212529;
            }
            QPushButton {
                background-color: #4361ee;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a56d4;
            }
            QPushButton#copyButton {
                background-color: #20c997;
            }
            QPushButton#copyButton:hover {
                background-color: #12b886;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                font-family: monospace;
            }
        """)
        
        # Создаем макет
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        
        # Заголовок
        header = QLabel(f"Результат хеширования {source_type}")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        
        # Информация об источнике
        source_info = QLabel(f"Источник: {source_name}")
        source_info.setWordWrap(True)
        layout.addWidget(source_info)
        
        # Результат хеширования
        result_label = QLabel("Хеш:")
        result_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(result_label)
        
        result_text = QTextEdit()
        result_text.setPlainText(hash_value)
        result_text.setReadOnly(True)
        result_text.setMinimumHeight(100)
        layout.addWidget(result_text)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        copy_button = QPushButton("Копировать хеш")
        copy_button.setObjectName("copyButton")
        copy_button.setIcon(QIcon.fromTheme("edit-copy"))
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(hash_value, copy_button))
        
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(dialog.accept)
        
        button_layout.addWidget(copy_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # Показываем диалог
        dialog.exec()
    
    def copy_to_clipboard(self, text, button):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        
        # Меняем текст кнопки на короткое время
        original_text = button.text()
        button.setText("Скопировано!")
        
        # Возвращаем исходный текст через 1.5 секунды
        QTimer.singleShot(1500, lambda: button.setText(original_text))
