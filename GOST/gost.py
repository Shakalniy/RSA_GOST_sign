import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from GOST import sign_file, check_sign, stribog


class GOSTFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Создание вкладок
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладка "Цифровая подпись"
        sign_frame = ttk.Frame(self.notebook)
        self.notebook.add(sign_frame, text="Цифровая подпись")
        
        # Вкладка "Хеширование"
        hash_frame = ttk.Frame(self.notebook)
        self.notebook.add(hash_frame, text="Хеширование")
        
        # Настройка вкладки "Цифровая подпись"
        self.setup_sign_frame(sign_frame)
        
        # Настройка вкладки "Хеширование"
        self.setup_hash_frame(hash_frame)
    
    def setup_sign_frame(self, parent):
        # Фрейм для файла
        file_frame = ttk.LabelFrame(parent, text="Выбор файла", padding=10)
        file_frame.pack(fill="x", pady=10)
        
        self.file_path = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.pack(side="left", padx=5)
        
        browse_button = ttk.Button(file_frame, text="Обзор",
                                 command=self.browse_file)
        browse_button.pack(side="left", padx=5)
        
        # Фрейм для кнопок операций
        operations_frame = ttk.LabelFrame(parent, text="Операции", padding=10)
        operations_frame.pack(fill="x", pady=10)
        
        sign_button = ttk.Button(operations_frame, 
                               text="Подписать файл",
                               command=self.sign_file)
        sign_button.pack(pady=5, fill="x")
        
        check_button = ttk.Button(operations_frame,
                                text="Проверить подпись",
                                command=self.check_signature)
        check_button.pack(pady=5, fill="x")
        
        # Статус операции
        self.status_var = tk.StringVar()
        status_label = ttk.Label(parent, textvariable=self.status_var,
                               wraplength=400)
        status_label.pack(pady=20)
    
    def setup_hash_frame(self, parent):
        # Основной фрейм с возможностью расширения
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(main_frame, text="Хеширование по ГОСТ 34.11-2018", padding=10)
        input_frame.pack(fill="x", pady=5)
        
        # Текстовое поле для ввода данных
        self.hash_input = tk.Text(input_frame, height=5, width=50)
        self.hash_input.pack(fill="x", pady=5)
        
        # Выбор размера хеш-кода
        size_frame = ttk.Frame(input_frame)
        size_frame.pack(fill="x", pady=5)
        
        ttk.Label(size_frame, text="Размер хеш-кода:").pack(side="left", padx=5)
        
        self.hash_size = tk.StringVar(value="256")
        sizes = ["256", "512"]
        size_dropdown = ttk.Combobox(size_frame, textvariable=self.hash_size, 
                                    values=sizes, state="readonly", width=10)
        size_dropdown.pack(side="left", padx=5)
        
        # Кнопка хеширования
        hash_button = ttk.Button(input_frame, text="Вычислить хеш",
                               command=self.compute_hash)
        hash_button.pack(pady=5)
        
        # Фрейм для вывода результата
        result_frame = ttk.LabelFrame(main_frame, text="Результат хеширования", padding=10)
        result_frame.pack(fill="both", expand=True, pady=5)
        
        # Текстовое поле для вывода результата с собственной прокруткой
        result_scroll = ttk.Scrollbar(result_frame)
        result_scroll.pack(side="right", fill="y")
        
        self.hash_result_text = tk.Text(result_frame, height=10, width=50, wrap=tk.WORD,
                                      yscrollcommand=result_scroll.set)
        self.hash_result_text.pack(side="left", fill="both", expand=True)
        result_scroll.config(command=self.hash_result_text.yview)
        
        # Делаем текстовое поле только для чтения
        self.hash_result_text.config(state="disabled")
    
    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.file_path.set(filename)
    
    def sign_file(self):
        if not self.file_path.get():
            messagebox.showerror("Ошибка", "Выберите файл для подписи")
            return
            
        try:
            sign_file.sign_file(self.file_path.get())
            self.status_var.set("Файл успешно подписан!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при подписи файла: {str(e)}")
            self.status_var.set("Ошибка при подписи файла")
    
    def check_signature(self):
        if not self.file_path.get():
            messagebox.showerror("Ошибка", "Выберите файл для проверки")
            return
            
        try:
            result = check_sign.check_sign(self.file_path.get())
            self.status_var.set(result)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при проверке подписи: {str(e)}")
            self.status_var.set("Ошибка при проверке подписи")
    
    def compute_hash(self):
        input_text = self.hash_input.get("1.0", tk.END).strip()
        hash_size = int(self.hash_size.get())
        
        if not input_text:
            messagebox.showerror("Ошибка", "Введите текст для хеширования")
            return
        
        try:
            h = stribog.start_stribog(input_text, hash_size)
            # Обновляем текстовое поле с результатом
            self.hash_result_text.config(state="normal")  # Разрешаем редактирование
            self.hash_result_text.delete("1.0", tk.END)  # Очищаем предыдущий результат
            self.hash_result_text.insert("1.0", f"Вычисленный хеш: h={h}")
            self.hash_result_text.config(state="disabled")  # Запрещаем редактирование
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при хешировании: {str(e)}")


def create_gost_frame(parent):
    return GOSTFrame(parent)


def gost():
    # Эта функция больше не используется напрямую, но оставлена для обратной совместимости
    pass