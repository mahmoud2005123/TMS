import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db_connection import connect_to_db
import re
import json
import logging
import csv

# Set up logging
logging.basicConfig(filename='supervisor_form.log',
                   level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class SupervisorForm:
    def __init__(self, parent=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Add New Supervisor")
        self.window.geometry("600x750")
        self.window.configure(bg="#f5f5f7")
        
        # Variables for storing original data for undo
        self.original_data = {}
        self.has_unsaved_changes = False
        
        # Bind keyboard shortcuts
        self.window.bind('<Control-s>', lambda e: self.submit())
        self.window.bind('<Control-z>', lambda e: self.undo())
        self.window.bind('<Escape>', lambda e: self.confirm_close())
        
        self.setup_ui()
        self.load_saved_data()
        
    def setup_ui(self):
        self.center_window()
        self.create_main_frame()
        self.setup_styles()
        self.create_title()
        self.create_info_frame()
        self.create_buttons()
        self.create_instructions()
        
    def center_window(self):
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww, wh = 600, 750
        x = (sw - ww) // 2
        y = (sh - wh) // 2
        self.window.geometry(f"{ww}x{wh}+{x}+{y}")

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), background="#f5f5f7")
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#f5f5f7")
        self.style.configure("TEntry", font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"))
        self.style.configure("Accent.TButton", 
                           background="#007bff", 
                           foreground="white", 
                           font=("Segoe UI", 11, "bold"))

    def create_title(self):
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill="x", pady=(0, 20))
        
        # Logo
        logo_canvas = tk.Canvas(title_frame, width=40, height=40, bg="#f5f5f7", highlightthickness=0)
        logo_canvas.pack(side="left", padx=(0, 10))
        logo_canvas.create_oval(5, 5, 35, 35, fill="#007bff", outline="#0056b3")
        logo_canvas.create_text(20, 20, text="S", fill="white", font=("Segoe UI", 16, "bold"))
        
        ttk.Label(title_frame, text="Supervisor Registration Form", style="Title.TLabel").pack(side="left")

    def create_info_frame(self):
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Supervisor Information", padding=10)
        self.info_frame.pack(fill="x", pady=(0, 15))

        # Variables for validation
        self.supervisor_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.position_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.type_var = tk.StringVar(value="internal")  # Default to internal

        # Supervisor Type
        type_frame = ttk.Frame(self.info_frame)
        type_frame.pack(fill="x", pady=5)
        ttk.Label(type_frame, text="Supervisor Type:").pack(side="left")
        ttk.Radiobutton(type_frame, text="Internal", variable=self.type_var, 
                       value="internal").pack(side="left", padx=10)
        ttk.Radiobutton(type_frame, text="External", variable=self.type_var, 
                       value="external").pack(side="left", padx=10)

        # Supervisor ID
        id_frame = ttk.Frame(self.info_frame)
        id_frame.pack(fill="x", pady=5)
        ttk.Label(id_frame, text="Supervisor ID:").pack(side="left")
        id_entry = ttk.Entry(id_frame, textvariable=self.supervisor_id_var)
        id_entry.pack(side="left", padx=5)
        self.id_label = ttk.Label(id_frame, text="Format: 6 digits", foreground="gray")
        self.id_label.pack(side="left")

        # Full Name
        name_frame = ttk.Frame(self.info_frame)
        name_frame.pack(fill="x", pady=5)
        ttk.Label(name_frame, text="Full Name:").pack(side="left")
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var)
        name_entry.pack(side="left", padx=5)
        self.name_label = ttk.Label(name_frame, text="", foreground="red")
        self.name_label.pack(side="left")

        # Department with search
        dept_frame = ttk.Frame(self.info_frame)
        dept_frame.pack(fill="x", pady=5)
        ttk.Label(dept_frame, text="Department:").pack(side="left")
        self.departments = ["Computer Science", "Business", "Engineering", "Medicine", 
                          "Law", "Architecture", "Economics", "Pharmacy", "Dentistry", "IT"]
        self.dept_combo = ttk.Combobox(dept_frame, textvariable=self.department_var, 
                                     values=self.departments, state="readonly")
        self.dept_combo.pack(side="left", padx=5, fill="x", expand=True)

        # Position
        position_frame = ttk.Frame(self.info_frame)
        position_frame.pack(fill="x", pady=5)
        ttk.Label(position_frame, text="Position:").pack(side="left")
        positions = ["Professor", "Associate Professor", "Assistant Professor", 
                    "Lecturer", "Industry Expert", "Senior Engineer"]
        self.position_combo = ttk.Combobox(position_frame, textvariable=self.position_var, 
                                         values=positions, state="readonly")
        self.position_combo.pack(side="left", padx=5, fill="x", expand=True)

        # Email
        email_frame = ttk.Frame(self.info_frame)
        email_frame.pack(fill="x", pady=5)
        ttk.Label(email_frame, text="Email:").pack(side="left")
        email_entry = ttk.Entry(email_frame, textvariable=self.email_var)
        email_entry.pack(side="left", padx=5)
        self.email_label = ttk.Label(email_frame, text="", foreground="red")
        self.email_label.pack(side="left")

        # Phone
        phone_frame = ttk.Frame(self.info_frame)
        phone_frame.pack(fill="x", pady=5)
        ttk.Label(phone_frame, text="Phone:").pack(side="left")
        phone_entry = ttk.Entry(phone_frame, textvariable=self.phone_var)
        phone_entry.pack(side="left", padx=5)
        self.phone_label = ttk.Label(phone_frame, text="", foreground="red")
        self.phone_label.pack(side="left")

        # Bind validation functions
        self.supervisor_id_var.trace('w', lambda *args: self.validate_id())
        self.name_var.trace('w', lambda *args: self.validate_name())
        self.email_var.trace('w', lambda *args: self.validate_email())
        self.phone_var.trace('w', lambda *args: self.validate_phone())
        
        # Mark changes
        for var in [self.supervisor_id_var, self.name_var, self.department_var, 
                   self.position_var, self.email_var, self.phone_var, self.type_var]:
            var.trace('w', lambda *args: self.mark_unsaved_changes())

    def create_buttons(self):
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill="x", pady=(15, 0))

        # Left side buttons
        left_buttons = ttk.Frame(buttons_frame)
        left_buttons.pack(side="left")
        
        ttk.Button(left_buttons, text="↩ Undo", command=self.undo).pack(side="left", padx=5)
        ttk.Button(left_buttons, text="Cancel", command=self.confirm_close).pack(side="left", padx=5)
        ttk.Button(left_buttons, text="Save Draft", command=self.save_draft).pack(side="left", padx=5)
        
        # Right side buttons
        right_buttons = ttk.Frame(buttons_frame)
        right_buttons.pack(side="right")
        
        ttk.Button(right_buttons, text="Import CSV", 
                  command=self.import_csv).pack(side="left", padx=5)
        self.submit_btn = ttk.Button(right_buttons, text="Add Supervisor", 
                                   command=self.submit, style="Accent.TButton")
        self.submit_btn.pack(side="left", padx=5)

    def create_instructions(self):
        instructions = """
        Instructions:
        1. Select supervisor type (Internal/External)
        2. Enter a unique 6-digit supervisor ID
        3. Enter the supervisor's full name (letters and spaces only)
        4. Select the department
        5. Select the position
        6. Enter a valid email address
        7. Enter a valid phone number (8-15 digits)
        
        Keyboard Shortcuts:
        • Ctrl + S: Submit form
        • Ctrl + Z: Undo last change
        • Esc: Cancel/Close
        
        Note: All fields are required and will be validated automatically.
        You can also import supervisor data from a CSV file.
        """
        instruction_frame = ttk.LabelFrame(self.main_frame, text="How to Use", padding=10)
        instruction_frame.pack(fill="x", pady=(15, 0))
        ttk.Label(instruction_frame, text=instructions, justify="left").pack()

    def validate_id(self):
        supervisor_id = self.supervisor_id_var.get().strip()
        if len(supervisor_id) == 6 and supervisor_id.isdigit():
            self.id_label.config(text="✓", foreground="green")
            return True
        else:
            self.id_label.config(text="Must be 6 digits", foreground="red")
            return False

    def validate_name(self):
        name = self.name_var.get().strip()
        if re.match(r'^[A-Za-z\s]{3,50}$', name):
            self.name_label.config(text="✓", foreground="green")
            return True
        else:
            self.name_label.config(text="Letters and spaces only (3-50 chars)", foreground="red")
            return False

    def validate_email(self):
        email = self.email_var.get().strip()
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.email_label.config(text="✓", foreground="green")
            return True
        else:
            self.email_label.config(text="Invalid email format", foreground="red")
            return False

    def validate_phone(self):
        phone = self.phone_var.get().strip()
        if phone.isdigit() and 8 <= len(phone) <= 15:
            self.phone_label.config(text="✓", foreground="green")
            return True
        else:
            self.phone_label.config(text="8-15 digits only", foreground="red")
            return False

    def validate_all(self):
        if not self.validate_id():
            messagebox.showwarning("Validation Error", "Please enter a valid Supervisor ID (6 digits)")
            return False
        if not self.validate_name():
            messagebox.showwarning("Validation Error", "Please enter a valid Name")
            return False
        if not self.validate_email():
            messagebox.showwarning("Validation Error", "Please enter a valid Email")
            return False
        if not self.validate_phone():
            messagebox.showwarning("Validation Error", "Please enter a valid Phone number")
            return False
        if not self.department_var.get():
            messagebox.showwarning("Validation Error", "Please select a Department")
            return False
        if not self.position_var.get():
            messagebox.showwarning("Validation Error", "Please select a Position")
            return False
        return True

    def mark_unsaved_changes(self, *args):
        self.has_unsaved_changes = True

    def save_draft(self):
        draft_data = {
            'supervisor_id': self.supervisor_id_var.get(),
            'name': self.name_var.get(),
            'department': self.department_var.get(),
            'position': self.position_var.get(),
            'email': self.email_var.get(),
            'phone': self.phone_var.get(),
            'type': self.type_var.get()
        }
        
        try:
            with open('supervisor_draft.json', 'w') as f:
                json.dump(draft_data, f)
            messagebox.showinfo("Success", "Draft saved successfully!")
        except Exception as e:
            logging.error(f"Error saving draft: {str(e)}")
            messagebox.showerror("Error", "Failed to save draft")

    def load_saved_data(self):
        try:
            with open('supervisor_draft.json', 'r') as f:
                draft_data = json.load(f)
                
            if messagebox.askyesno("Load Draft", "Would you like to load the saved draft?"):
                self.supervisor_id_var.set(draft_data['supervisor_id'])
                self.name_var.set(draft_data['name'])
                self.department_var.set(draft_data['department'])
                self.position_var.set(draft_data['position'])
                self.email_var.set(draft_data['email'])
                self.phone_var.set(draft_data['phone'])
                self.type_var.set(draft_data['type'])
                
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.error(f"Error loading draft: {str(e)}")

    def import_csv(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("CSV Files", "*.csv")],
                title="Select CSV File"
            )
            
            if not file_path:
                return
                
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                first_row = next(reader)
                
                # Validate CSV structure
                required_fields = ['supervisor_id', 'name', 'department', 'position', 
                                 'email', 'phone', 'type']
                if not all(field in first_row for field in required_fields):
                    messagebox.showerror("Error", "Invalid CSV format. Please check the template.")
                    return
                
                # Set form data from first row
                self.supervisor_id_var.set(first_row['supervisor_id'])
                self.name_var.set(first_row['name'])
                self.department_var.set(first_row['department'])
                self.position_var.set(first_row['position'])
                self.email_var.set(first_row['email'])
                self.phone_var.set(first_row['phone'])
                self.type_var.set(first_row['type'])
                
                messagebox.showinfo("Success", "Data imported successfully!")
                
        except Exception as e:
            logging.error(f"Error importing CSV: {str(e)}")
            messagebox.showerror("Error", f"Failed to import CSV: {str(e)}")

    def submit(self, event=None):
        if not self.validate_all():
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            # Check if supervisor ID already exists
            table_name = "internal_supervisors" if self.type_var.get() == "internal" else "external_supervisors"
            cursor.execute(f"SELECT supervisor_id FROM {table_name} WHERE supervisor_id = %s", 
                         (int(self.supervisor_id_var.get()),))
            if cursor.fetchone():
                messagebox.showerror("Error", "Supervisor ID already exists!")
                return

            # Insert supervisor data
            cursor.execute(f"""
                INSERT INTO {table_name} (
                    supervisor_id, supervisor_name, department, position,
                    email, phone
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                int(self.supervisor_id_var.get()),
                self.name_var.get().strip(),
                self.department_var.get(),
                self.position_var.get(),
                self.email_var.get().strip(),
                self.phone_var.get().strip()
            ))

            conn.commit()
            conn.close()

            # Delete draft if exists
            try:
                import os
                os.remove('supervisor_draft.json')
            except:
                pass

            messagebox.showinfo("Success", "Supervisor added successfully!")
            self.window.destroy()

        except Exception as e:
            logging.error(f"Error submitting supervisor data: {str(e)}")
            messagebox.showerror("Error", f"Failed to add supervisor: {str(e)}")

    def undo(self, event=None):
        # Implement undo functionality
        pass

    def confirm_close(self, event=None):
        if self.has_unsaved_changes:
            if messagebox.askyesno("Confirm Close", 
                                 "You have unsaved changes. Do you want to save a draft before closing?"):
                self.save_draft()
        self.window.destroy()

def open_insert_supervisor_form():
    SupervisorForm() 