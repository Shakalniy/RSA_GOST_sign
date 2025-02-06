import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from RSA import sign_file, check_sign


class RSAFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Фрейм для файла
        file_frame = ttk.LabelFrame(self, text="Выбор файла", padding=10)
        file_frame.pack(fill="x", pady=10)
        
        self.file_path = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.pack(side="left", padx=5)
        
        browse_button = ttk.Button(file_frame, text="Обзор",
                                 command=self.browse_file)
        browse_button.pack(side="left", padx=5)
        
        # Фрейм для кнопок операций
        operations_frame = ttk.LabelFrame(self, text="Операции", padding=10)
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
        status_label = ttk.Label(self, textvariable=self.status_var,
                               wraplength=400)
        status_label.pack(pady=20)

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


def create_rsa_frame(parent):
    return RSAFrame(parent)
