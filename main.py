import tkinter as tk
from tkinter import ttk, messagebox
import RSA.rsa as rsa
import GOST.gost as gost

class SignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Signature")
        self.root.geometry("500x600")
        
        self.root.option_add('*Font', 'Arial 10')
        
        self.style = ttk.Style()
        self.style.configure('TButton', padding=10, font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('TFrame', font=('Arial', 10))
        self.style.configure('TLabelframe', font=('Arial', 10))
        self.style.configure('TLabelframe.Label', font=('Arial', 10))
        self.style.configure('TNotebook', font=('Arial', 10))
        self.style.configure('TNotebook.Tab', font=('Arial', 10))
        
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_menu_frame()
        
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(fill="both", expand=True)
        
        self.show_main_menu()
        
    def create_menu_frame(self):
        self.menu_frame = ttk.Frame(self.main_container)
        self.menu_frame.pack(fill="x", pady=(0, 20))
        
        self.back_button = ttk.Button(self.menu_frame, text="Back",
                                    command=self.show_main_menu)
        
        self.title_label = ttk.Label(self.menu_frame, text="Select Signature Method",
                                   style='TLabel')
        self.title_label.pack(pady=10)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def show_main_menu(self):
        self.clear_content()
        self.back_button.pack_forget()
        self.title_label.config(text="Select Signature Method")
        
        ttk.Button(self.content_frame, text="RSA Digital Signature",
                  command=self.show_rsa_frame).pack(pady=10)
        ttk.Button(self.content_frame, text="GOST Digital Signature",
                  command=self.show_gost_frame).pack(pady=10)
        ttk.Button(self.content_frame, text="Exit",
                  command=self.root.quit).pack(pady=10)

    def show_rsa_frame(self):
        self.clear_content()
        self.back_button.pack(side="left", padx=(0, 10))
        self.title_label.config(text="RSA Digital Signature")
        
        # Create RSA frame
        rsa_frame = rsa.create_rsa_frame(self.content_frame)
        rsa_frame.pack(fill="both", expand=True)

    def show_gost_frame(self):
        self.clear_content()
        self.back_button.pack(side="left", padx=(0, 10))
        self.title_label.config(text="GOST Digital Signature")
        
        gost_frame = gost.create_gost_frame(self.content_frame)
        gost_frame.pack(fill="both", expand=True)

def main():
    root = tk.Tk()
    app = SignatureApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
