import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db
from tkcalendar import DateEntry
from datetime import datetime

def open_insert_report_form():
    window = tk.Toplevel()
    window.title("Add Training Report")
    window.geometry("500x450")
    window.configure(bg="#f5f5f7")

    def center(win):
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        ww, wh = 500, 450
        win.geometry(f"{ww}x{wh}+{(sw - ww) // 2}+{(sh - wh) // 2}")

    center(window)

    style = ttk.Style()
    style.configure("TLabel", background="#f5f5f7", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10, "bold"))

    # Student Selection
    ttk.Label(window, text="👨‍🎓 Student ID").pack(pady=5)
    student_combo = ttk.Combobox(window, width=40)
    student_combo.pack()

    # Organization Selection
    ttk.Label(window, text="🏢 Organization ID").pack(pady=5)
    org_combo = ttk.Combobox(window, width=40)
    org_combo.pack()

    # Date Selection with Calendar
    ttk.Label(window, text="📅 Report Date").pack(pady=5)
    date_picker = DateEntry(window, width=38, background='darkblue',
                          foreground='white', borderwidth=2,
                          mindate=datetime(2023, 1, 1),
                          maxdate=datetime(2023, 12, 31))
    date_picker.pack()

    # Report Text
    ttk.Label(window, text="📝 Report Text").pack(pady=5)
    text_entry = tk.Text(window, height=5, width=50)
    text_entry.pack()

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        
        # Get students list
        cursor.execute("SELECT student_id, student_name FROM students")
        students = cursor.fetchall()
        student_combo['values'] = [f"{row[0]} - {row[1]}" for row in students]
        
        # Get organizations list
        cursor.execute("SELECT organization_id, organization_name FROM organizations")
        orgs = cursor.fetchall()
        org_combo['values'] = [f"{row[0]} - {row[1]}" for row in orgs]
        
        conn.close()
    except Exception as e:
        messagebox.showerror("DB Error", str(e))
        window.destroy()
        return

    def validate_inputs():
        if not student_combo.get():
            messagebox.showwarning("Validation Error", "Please select a student")
            return False
        if not org_combo.get():
            messagebox.showwarning("Validation Error", "Please select an organization")
            return False
        if not text_entry.get("1.0", tk.END).strip():
            messagebox.showwarning("Validation Error", "Please enter report text")
            return False
        return True

    def submit():
        if not validate_inputs():
            return
            
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            
            # Get next report ID
            cursor.execute("SELECT MAX(report_id) FROM training_reports")
            new_id = (cursor.fetchone()[0] or 0) + 1
            
            # Extract student_id from combo selection
            student_id = int(student_combo.get().split(' - ')[0])
            
            # Extract organization_id from combo selection
            org_id = int(org_combo.get().split(' - ')[0])
            
            # Format date
            report_date = date_picker.get_date().strftime('%Y-%m-%d')
            
            cursor.execute("""
                INSERT INTO training_reports (report_id, student_id, organization_id, report_date, report_text)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                new_id,
                student_id,
                org_id,
                report_date,
                text_entry.get("1.0", tk.END).strip()
            ))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Report added successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Insert Failed", str(e))

    submit_btn = ttk.Button(window, text="Submit Report", command=submit)
    submit_btn.pack(pady=20)

    # Add some instructions
    instructions = """
    Instructions:
    1. Select the student from the dropdown
    2. Select the organization from the dropdown
    3. Choose a date between Jan 1, 2023 and Dec 31, 2023
    4. Enter the report text
    5. Click Submit
    """
    ttk.Label(window, text=instructions, background="#f5f5f7", justify=tk.LEFT).pack(pady=10)
