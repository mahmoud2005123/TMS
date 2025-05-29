# Style improvements for admin_panel.py

import tkinter as tk
from tkinter import ttk, font
from db_connection import connect_to_db

def open_admin_view():
    window = tk.Toplevel()
    window.title("Training Report Management")
    window.configure(bg="#f5f5f7")
    
    # Set window size and center it
    window_width, window_height = 1000, 600
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Create styles
    style = ttk.Style()
    
    # Configure styles for components
    style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background="#f5f5f7")
    style.configure("TFrame", background="#f5f5f7")
    style.configure("Search.TEntry", padding=8, font=("Segoe UI", 10))
    
    # Configure Treeview style
    style.configure("Treeview", 
                    background="#ffffff",
                    foreground="#333333",
                    rowheight=30,
                    fieldbackground="#ffffff",
                    font=("Segoe UI", 10))
    style.configure("Treeview.Heading", 
                    font=("Segoe UI", 10, "bold"),
                    background="#e9e9e9",
                    foreground="#333333",
                    padding=8)
    style.map("Treeview", background=[("selected", "#3498db")])
    
    # Main container
    main_frame = ttk.Frame(window, style="TFrame")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Header frame
    header_frame = ttk.Frame(main_frame, style="TFrame")
    header_frame.pack(fill="x", pady=(0, 15))
    
    # Title
    ttk.Label(header_frame, text="Training Reports Overview", style="Header.TLabel").pack(side="left")
    
    # Search frame
    search_frame = ttk.Frame(header_frame, style="TFrame")
    search_frame.pack(side="right")
    
    ttk.Label(search_frame, text="Search:", background="#f5f5f7").pack(side="left", padx=(0, 8))
    search_entry = ttk.Entry(search_frame, width=25, style="Search.TEntry")
    search_entry.pack(side="left", padx=(0, 5))
    
    # Filter frame below header
    filter_frame = ttk.Frame(main_frame, style="TFrame")
    filter_frame.pack(fill="x", pady=(0, 15))
    
    # Filter options
    ttk.Label(filter_frame, text="Filter by:", background="#f5f5f7").pack(side="left", padx=(0, 8))
    
    org_var = tk.StringVar(value="All Organizations")
    org_combo = ttk.Combobox(filter_frame, textvariable=org_var, width=20, state="readonly")
    org_combo.pack(side="left", padx=(0, 15))
    
    score_var = tk.StringVar(value="All Scores")
    score_combo = ttk.Combobox(filter_frame, textvariable=score_var, width=15, state="readonly")
    score_combo.pack(side="left")
    
    # Set some sample values for dropdowns
    org_combo["values"] = ["All Organizations", "Organization A", "Organization B", "Organization C"]
    score_combo["values"] = ["All Scores", "90+", "80-89", "70-79", "Below 70"]
    
    # Create a frame for the treeview and scrollbar
    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True)
    
    # Create the treeview
    columns = ("Student Name", "Organization", "Report Date", "Score", "Comments")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    
    # Set column widths and headings
    column_widths = [150, 150, 100, 80, 300]
    for i, col in enumerate(columns):
        tree.column(col, width=column_widths[i], anchor=tk.W)
        tree.heading(col, text=col, anchor=tk.W)
    
    # Add vertical scrollbar
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    
    # Pack scrollbar and tree
    vsb.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)
    
    # Add horizontal scrollbar
    hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    hsb.pack(fill="x")
    
    # Function to handle search
    def handle_search(event=None):
        search_term = search_entry.get().lower()
        tree.delete(*tree.get_children())
        
        for row in all_data:
            if search_term == "" or any(search_term in str(item).lower() for item in row):
                tree.insert("", "end", values=row)
    
    # Bind search entry to search function
    search_entry.bind("<Return>", handle_search)
    
    # Function to handle filter changes
    def handle_filter(event=None):
        org_filter = org_var.get()
        score_filter = score_var.get()
        
        tree.delete(*tree.get_children())
        
        for row in all_data:
            add_row = True
            
            # Apply organization filter
            if org_filter != "All Organizations" and row[1] != org_filter:
                add_row = False
                
            # Apply score filter
            if score_filter != "All Scores":
                score = float(row[3])
                if score_filter == "90+" and score < 90:
                    add_row = False
                elif score_filter == "80-89" and (score < 80 or score >= 90):
                    add_row = False
                elif score_filter == "70-79" and (score < 70 or score >= 80):
                    add_row = False
                elif score_filter == "Below 70" and score >= 70:
                    add_row = False
            
            if add_row:
                tree.insert("", "end", values=row)
    
    # Bind filter comboboxes to filter function
    org_combo.bind("<<ComboboxSelected>>", handle_filter)
    score_combo.bind("<<ComboboxSelected>>", handle_filter)
    
    # Action buttons frame
    action_frame = ttk.Frame(main_frame, style="TFrame")
    action_frame.pack(fill="x", pady=(15, 0))
    
    # Style for buttons
    style.configure("Action.TButton", font=("Segoe UI", 10), padding=6)
    
    # Action buttons
    ttk.Button(action_frame, text="Export Selected", style="Action.TButton").pack(side="left", padx=(0, 10))
    ttk.Button(action_frame, text="Print Report", style="Action.TButton").pack(side="left", padx=(0, 10))
    ttk.Button(action_frame, text="Close", style="Action.TButton", command=window.destroy).pack(side="right")
    
    # Status bar
    status_frame = ttk.Frame(main_frame, style="TFrame")
    status_frame.pack(fill="x", pady=(15, 0))
    status_var = tk.StringVar(value="Ready")
    status_label = ttk.Label(status_frame, textvariable=status_var, background="#f5f5f7", foreground="#888888")
    status_label.pack(side="left")
    
    # Alternate row colors function
    def alternating_row_colors():
        for i, item in enumerate(tree.get_children()):
            if i % 2 == 0:
                tree.item(item, tags=("evenrow",))
            else:
                tree.item(item, tags=("oddrow",))
        
        tree.tag_configure("evenrow", background="#f9f9f9")
        tree.tag_configure("oddrow", background="#ffffff")
    
    # Get data from database
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.student_name, o.organization_name, tr.report_date, e.evaluation_score, e.evaluation_comments
            FROM students s
            JOIN training_reports tr ON s.student_id = tr.student_id
            JOIN organizations o ON tr.organization_id = o.organization_id
            JOIN evaluations e ON tr.report_id = e.report_id
            ORDER BY tr.report_date DESC
        """)
        
        all_data = cursor.fetchall()
        
        # Get unique organizations for filter
        cursor.execute("SELECT DISTINCT organization_name FROM organizations ORDER BY organization_name")
        orgs = ["All Organizations"] + [row[0] for row in cursor.fetchall()]
        org_combo["values"] = orgs
        
        conn.close()
        
        # Insert data into treeview
        for row in all_data:
            tree.insert("", "end", values=row)
            
        alternating_row_colors()
        status_var.set(f"Displaying {len(all_data)} records")
        
    except Exception as e:
        status_var.set(f"Error: {e}")
    
    # Make the window responsive
    for i in range(len(columns)):
        main_frame.columnconfigure(i, weight=1)
    
    window.mainloop()