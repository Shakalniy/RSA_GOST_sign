import tkinter as tk
from tkinter import ttk, messagebox
import RSA.rsa as rsa
import GOST.gost as gost

class SignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Цифровая подпись")
        self.root.geometry("500x600")
        
        # Создание стиля
        self.style = ttk.Style()
        self.style.configure('TButton', padding=10, font=('Helvetica', 10))
        self.style.configure('TLabel', font=('Helvetica', 12))
        
        # Создание главного контейнера
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Создание меню выбора
        self.create_menu_frame()
        
        # Создание фрейма для контента
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(fill="both", expand=True)
        
        # Показываем начальное меню
        self.show_main_menu()
        
    def create_menu_frame(self):
        self.menu_frame = ttk.Frame(self.main_container)
        self.menu_frame.pack(fill="x", pady=(0, 20))
        
        # Кнопка возврата в главное меню (изначально скрыта)
        self.back_button = ttk.Button(self.menu_frame, text="← Назад",
                                    command=self.show_main_menu)
        
        # Заголовок текущего раздела
        self.title_label = ttk.Label(self.menu_frame, text="Выберите метод подписи",
                                   style='TLabel')
        self.title_label.pack(pady=10)

    def clear_content(self):
        # Очищаем фрейм контента
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def show_main_menu(self):
        self.clear_content()
        self.back_button.pack_forget()  # Скрываем кнопку "Назад"
        self.title_label.config(text="Выберите метод подписи")
        
        # Создаем кнопки главного меню
        ttk.Button(self.content_frame, text="Цифровая подпись RSA",
                  command=self.show_rsa_frame).pack(pady=10)
        ttk.Button(self.content_frame, text="Цифровая подпись ГОСТ",
                  command=self.show_gost_frame).pack(pady=10)
        ttk.Button(self.content_frame, text="Выход",
                  command=self.root.quit).pack(pady=10)

    def show_rsa_frame(self):
        self.clear_content()
        self.back_button.pack(side="left", padx=(0, 10))  # Показываем кнопку "Назад"
        self.title_label.config(text="RSA Цифровая подпись")
        
        # Создаем фрейм RSA
        rsa_frame = rsa.create_rsa_frame(self.content_frame)
        rsa_frame.pack(fill="both", expand=True)

    def show_gost_frame(self):
        self.clear_content()
        self.back_button.pack(side="left", padx=(0, 10))  # Показываем кнопку "Назад"
        self.title_label.config(text="ГОСТ Цифровая подпись")
        
        gost_frame = gost.create_gost_frame(self.content_frame)
        gost_frame.pack(fill="both", expand=True)

def main():
    root = tk.Tk()
    app = SignatureApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
