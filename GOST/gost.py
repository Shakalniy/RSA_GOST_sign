import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from GOST import sign_file, check_sign, stribog


class GOSTFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('TLabelframe', font=('Arial', 10))
        self.style.configure('TLabelframe.Label', font=('Arial', 10))
        self.style.configure('TNotebook', font=('Arial', 10))
        self.style.configure('TNotebook.Tab', font=('Arial', 10))
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        sign_frame = ttk.Frame(self.notebook)
        self.notebook.add(sign_frame, text="Digital Signature")
        
        hash_frame = ttk.Frame(self.notebook)
        self.notebook.add(hash_frame, text="Hashing")
        
        self.setup_sign_frame(sign_frame)
        
        self.setup_hash_frame(hash_frame)
    
    def setup_sign_frame(self, parent):
        file_frame = ttk.LabelFrame(parent, text="File Selection", padding=10)
        file_frame.pack(fill="x", pady=10)
        
        self.file_path = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path)
        file_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        browse_button = ttk.Button(file_frame, text="Browse",
                                 command=self.browse_file)
        browse_button.pack(side="left", padx=5)
        
        operations_frame = ttk.LabelFrame(parent, text="Operations", padding=10)
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
        status_label = ttk.Label(parent, textvariable=self.status_var,
                               wraplength=400)
        status_label.pack(pady=20)
    
    def setup_hash_frame(self, parent):
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        input_frame = ttk.LabelFrame(main_frame, text="Hashing by GOST 34.11-2018", padding=10)
        input_frame.pack(fill="x", pady=5)
        
        self.hash_input = tk.Text(input_frame, height=5, width=50, font=('Arial', 10))
        self.hash_input.pack(fill="x", pady=5)
        
        size_frame = ttk.Frame(input_frame)
        size_frame.pack(fill="x", pady=5)
        
        ttk.Label(size_frame, text="Hash size:").pack(side="left", padx=5)
        
        self.hash_size = tk.StringVar(value="256")
        sizes = ["256", "512"]
        size_dropdown = ttk.Combobox(size_frame, textvariable=self.hash_size,
                                    values=sizes, state="readonly", width=10)
        size_dropdown.pack(side="left", padx=5)
        
        hash_button = ttk.Button(input_frame, text="Calculate Hash",
                               command=self.compute_hash)
        hash_button.pack(pady=5)
        
        result_frame = ttk.LabelFrame(main_frame, text="Hashing Result", padding=10)
        result_frame.pack(fill="both", expand=True, pady=5)
        
        result_scroll = ttk.Scrollbar(result_frame)
        result_scroll.pack(side="right", fill="y")
        
        self.hash_result_text = tk.Text(result_frame, height=10, width=50, yscrollcommand=result_scroll.set, font=('Arial', 10))
        self.hash_result_text.pack(side="left", fill="both", expand=True)
        result_scroll.config(command=self.hash_result_text.yview)
        
        self.hash_result_text.config(state="disabled")
    
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
            messagebox.showerror("Error", f"Error signing file: {str(e)}")
            self.status_var.set("Error signing file")
    
    def check_signature(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a file to check")
            return
        
        try:
            result = check_sign.check_sign(self.file_path.get())
            self.status_var.set(result)
            if result == "Signature is valid":
                messagebox.showinfo("Success", result)
            elif result == "Signature not found":
                messagebox.showwarning("Warning", result)
            else:
                messagebox.showwarning("Warning", result)
        except Exception as e:
            messagebox.showerror("Error", f"Error checking signature: {str(e)}")
            self.status_var.set("Error checking signature")
    
    def compute_hash(self):
        input_text = self.hash_input.get("1.0", tk.END).strip()
        hash_size = int(self.hash_size.get())
        
        if not input_text:
            messagebox.showerror("Error", "Please enter text to hash")
            return
        
        try:
            h = stribog.start_stribog(input_text, hash_size)
            
            self.hash_result_text.config(state="normal")  # Allow editing
            self.hash_result_text.delete("1.0", tk.END)  # Clear previous result
            self.hash_result_text.insert("1.0", f"Calculated hash: h={h}")
            self.hash_result_text.config(state="disabled")  # Disallow editing
        except Exception as e:
            messagebox.showerror("Error", f"Error hashing: {str(e)}")


def create_gost_frame(parent):
    return GOSTFrame(parent)
