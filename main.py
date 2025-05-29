import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db, verify_connection
from dashboard import start_dashboard
import os
from PIL import Image, ImageTk

def login():
    username = entry_user.get()
    password = entry_pass.get()

    if not username or not password:
        messagebox.showwarning("Input Required", "Please enter both username and password")
        return

    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Login Successful", f"Welcome, {username}")
            root.destroy()
            start_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            entry_pass.delete(0, tk.END)
            entry_pass.focus()

    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")

def main():
    if not verify_connection():
        messagebox.showerror("Error", "Could not connect to database. Please check your database connection.")
        return

    global root, entry_user, entry_pass
    root = tk.Tk()
    root.title("Training Management System")
    root.configure(bg="#f5f5f7")
    root.resizable(False, False)

    def center_window(width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")

    center_window(450, 380)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#f5f5f7")
    style.configure("TLabel", font=("Segoe UI", 11), background="#f5f5f7")
    style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background="#f5f5f7")
    style.configure("TButton", font=("Segoe UI", 11), padding=8)
    style.configure("TEntry", padding=8, font=("Segoe UI", 10))

    main_frame = ttk.Frame(root, style="TFrame")
    main_frame.pack(fill="both", expand=True, padx=25, pady=25)

    header_frame = ttk.Frame(main_frame, style="TFrame")
    header_frame.pack(fill="x", pady=(0, 20))

    try:
        logo_canvas = tk.Canvas(header_frame, width=60, height=60, bg="#f5f5f7", highlightthickness=0)
        logo_canvas.pack(side="left", padx=(0, 15))
        logo_canvas.create_oval(5, 5, 55, 55, fill="#3498db", outline="#2980b9", width=2)
        logo_canvas.create_text(30, 30, text="TMS", fill="white", font=("Segoe UI", 14, "bold"))
    except Exception:
        pass

    ttk.Label(header_frame, text="Training Management System", style="Header.TLabel").pack(side="left", pady=10)

    form_frame = ttk.Frame(main_frame, style="TFrame")
    form_frame.pack(fill="x", pady=10)

    style.configure("Field.TFrame", background="#f5f5f7")

    user_frame = ttk.Frame(form_frame, style="Field.TFrame")
    user_frame.pack(fill="x", pady=10)
    ttk.Label(user_frame, text="👤", font=("Segoe UI", 12), background="#f5f5f7").pack(side="left", padx=(0, 10))
    ttk.Label(user_frame, text="Username:", background="#f5f5f7").pack(side="left", padx=(0, 10))
    entry_user = ttk.Entry(user_frame, width=25, font=("Segoe UI", 10))
    entry_user.pack(side="left", fill="x", expand=True)

    pass_frame = ttk.Frame(form_frame, style="Field.TFrame")
    pass_frame.pack(fill="x", pady=10)
    ttk.Label(pass_frame, text="🔒", font=("Segoe UI", 12), background="#f5f5f7").pack(side="left", padx=(0, 10))
    ttk.Label(pass_frame, text="Password:", background="#f5f5f7").pack(side="left", padx=(0, 10))
    entry_pass = ttk.Entry(pass_frame, width=25, font=("Segoe UI", 10), show="•")
    entry_pass.pack(side="left", fill="x", expand=True)

    button_frame = ttk.Frame(main_frame, style="TFrame")
    button_frame.pack(fill="x", pady=(25, 0))

    style.configure("Login.TButton", font=("Segoe UI", 11, "bold"), background="#3498db", foreground="white")
    style.map("Login.TButton",
        background=[("active", "#2980b9"), ("pressed", "#1c6ea4")],
        foreground=[("active", "white"), ("pressed", "white")])

    login_button = ttk.Button(button_frame, text="Sign In", command=login, style="Login.TButton", width=15)
    login_button.pack(pady=10)

    footer_frame = ttk.Frame(main_frame, style="TFrame")
    footer_frame.pack(fill="x", pady=(30, 0))
    ttk.Label(footer_frame, text="© 2025 Training Management System",
              font=("Segoe UI", 8), foreground="#888888", background="#f5f5f7").pack()

    entry_user.focus()
    root.bind("<Return>", lambda event: login())

    root.mainloop()

if __name__ == "__main__":
    main()
