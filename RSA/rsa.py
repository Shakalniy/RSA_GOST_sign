import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from RSA import sign_file, check_sign


class RSAFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('TLabelframe', font=('Arial', 10))
        self.style.configure('TLabelframe.Label', font=('Arial', 10))
        
        file_frame = ttk.LabelFrame(self, text="File Selection", padding=10)
        file_frame.pack(fill="x", pady=10)
        
        self.file_path = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path)
        file_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        browse_button = ttk.Button(file_frame, text="Browse",
                                 command=self.browse_file)
        browse_button.pack(side="left", padx=5)
        
        operations_frame = ttk.LabelFrame(self, text="Operations", padding=10)
        operations_frame.pack(fill="x", pady=10)
        
        sign_button = ttk.Button(operations_frame, 
                               text="Sign File",
                               command=self.sign_file)
        sign_button.pack(pady=5, fill="x")
        
        check_button = ttk.Button(operations_frame,
                                text="Check Signature",
                                command=self.check_signature)
        check_button.pack(pady=5, fill="x")
        
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
            messagebox.showerror("Error", "Please select a file to sign")
            return
        
        try:
            sign_file.sign_file(self.file_path.get())
            self.status_var.set("File signed successfully")
            messagebox.showinfo("Success", "File signed successfully")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def check_signature(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a file to check")
            return
        
        try:
            result = check_sign.check_sign(self.file_path.get())
            self.status_var.set("Signature is valid" if result else "Signature is invalid")
            if result:
                messagebox.showinfo("Success", "Signature is valid")
            else:
                messagebox.showwarning("Warning", "Signature is invalid")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))


def create_rsa_frame(parent):
    return RSAFrame(parent)
