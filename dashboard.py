import tkinter as tk
from tkinter import ttk
from admin_panel import open_admin_view
from report_export import export_reports
from insert_report_form import open_insert_report_form
from insert_evaluation_form import open_insert_evaluation_form
from call_procedure_avg import open_avg_score_form
from insert_student_form import open_insert_student_form
from upload_students_gui import open_upload_students
from manual_use import open_manual_use
import sys

def start_dashboard():
    window = tk.Tk()
    window.title("Training Management System")
    window.configure(bg="#f5f5f7")

    def center_window(width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    center_window(800, 600)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TFrame", background="#f5f5f7")
    style.configure("TLabel", font=("Segoe UI", 11), background="#f5f5f7")
    style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), background="#f5f5f7", foreground="#333333")
    style.configure("Subheader.TLabel", font=("Segoe UI", 12), background="#f5f5f7", foreground="#666666")

    style.configure("Menu.TButton", font=("Segoe UI", 11), padding=10)
    style.map("Menu.TButton",
              background=[("active", "#e1e1e1"), ("pressed", "#d0d0d0")],
              relief=[("pressed", "sunken"), ("!pressed", "raised")])

    main_frame = ttk.Frame(window, style="TFrame")
    main_frame.pack(fill="both", expand=True)

    nav_frame = ttk.Frame(main_frame, style="TFrame", width=200)
    nav_frame.pack(side="left", fill="y", padx=15, pady=15)
    nav_frame.pack_propagate(False)

    content_frame = ttk.Frame(main_frame, style="TFrame")
    content_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

    logo_canvas = tk.Canvas(nav_frame, width=60, height=60, bg="#f5f5f7", highlightthickness=0)
    logo_canvas.pack(anchor="center", pady=(20, 5))
    logo_canvas.create_oval(5, 5, 55, 55, fill="#3498db", outline="#2980b9", width=2)
    logo_canvas.create_text(30, 30, text="TMS", fill="white", font=("Segoe UI", 14, "bold"))

    ttk.Label(nav_frame, text="Training Management", style="Header.TLabel",
              font=("Segoe UI", 14, "bold"), foreground="#333333").pack(pady=(0, 30))

    menu_frame = ttk.Frame(nav_frame, style="TFrame")
    menu_frame.pack(fill="x", pady=5)

    button_data = [
        ("👤 Admin Panel", open_admin_view),
        ("👨‍🎓 Add Student", open_insert_student_form),
        ("📝 Insert Report", open_insert_report_form),
        ("⭐ Add Evaluation", open_insert_evaluation_form),
        ("📊 Get Avg Score", open_avg_score_form),
        ("📁 Export Reports", export_reports),
        ("📤 Upload Students", open_upload_students),
        ("❓ Manual Use", open_manual_use),
        ("🚪 Exit System", window.destroy)
    ]

    for text, command in button_data:
        button = ttk.Button(menu_frame, text=text, command=command, style="Menu.TButton", width=20)
        button.pack(fill="x", pady=5)

    ttk.Label(content_frame, text="Welcome to Training Management System",
              style="Header.TLabel").pack(pady=(40, 10))
    ttk.Label(content_frame, text="Select an option from the menu to get started",
              style="Subheader.TLabel").pack(pady=(0, 30))

    stats_frame = ttk.Frame(content_frame, style="TFrame")
    stats_frame.pack(fill="x", pady=20)

    style.configure("Card.TFrame", background="white", relief="raised")

    for i in range(2):
        stats_frame.columnconfigure(i, weight=1)

    stat_data = [
        ("Total Reports", "125", "#3498db"),
        ("Avg Score", "87.5", "#2ecc71"),
        ("Organizations", "18", "#e74c3c"),
        ("Students", "42", "#f39c12")
    ]

    row, col = 0, 0
    for title, value, color in stat_data:
        card = ttk.Frame(stats_frame, style="Card.TFrame")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        indicator = tk.Frame(card, width=5, bg=color)
        indicator.pack(side="left", fill="y")

        card_content = ttk.Frame(card)
        card_content.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        ttk.Label(card_content, text=title, font=("Segoe UI", 12), background="white").pack(anchor="w")
        ttk.Label(card_content, text=value, font=("Segoe UI", 24, "bold"), foreground=color, background="white").pack(anchor="w")

        col += 1
        if col > 1:
            col = 0
            row += 1

    footer_frame = ttk.Frame(content_frame, style="TFrame")
    footer_frame.pack(side="bottom", fill="x", pady=10)
    ttk.Label(footer_frame, text="© 2025 Training Management System",
              font=("Segoe UI", 8), foreground="#888888", background="#f5f5f7").pack(side="right")

    window.mainloop()
