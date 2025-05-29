import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db
from tkcalendar import DateEntry
from datetime import datetime
import re
import logging
import json

# Set up logging
logging.basicConfig(filename='evaluation_form.log',
                   level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class EvaluationForm:
    def __init__(self, parent=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Add Training Evaluation")
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
        self.load_data()
        
    def setup_ui(self):
        self.center_window()
        self.create_main_frame()
        self.setup_styles()
        self.create_title()
        self.create_info_frame()
        self.create_eval_frame()
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
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), background="#f5f5f7")
        self.style.configure("TLabel", font=("Segoe UI", 10), background="#f5f5f7")
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
        logo_canvas.create_text(20, 20, text="E", fill="white", font=("Segoe UI", 16, "bold"))
        
        ttk.Label(title_frame, text="Training Evaluation Form", style="Title.TLabel").pack(side="left")

    def create_info_frame(self):
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Training Information", padding=10)
        self.info_frame.pack(fill="x", pady=(0, 15))

        # Report Selection
        report_frame = ttk.Frame(self.info_frame)
        report_frame.pack(fill="x", pady=5)
        ttk.Label(report_frame, text="📄 Select Report:").pack(side="left", padx=(0, 10))
        self.report_combo = ttk.Combobox(report_frame, width=40, state="readonly")
        self.report_combo.pack(side="left", fill="x", expand=True)
        self.report_combo.bind('<<ComboboxSelected>>', self.on_report_select)

        # Student Info Display
        self.student_info = ttk.Label(self.info_frame, text="", style="TLabel")
        self.student_info.pack(fill="x", pady=5)

        # Supervisor Selection
        supervisor_frame = ttk.Frame(self.info_frame)
        supervisor_frame.pack(fill="x", pady=5)
        ttk.Label(supervisor_frame, text="👨‍🏫 Supervisor:").pack(side="left", padx=(0, 10))
        self.supervisor_combo = ttk.Combobox(supervisor_frame, width=40, state="readonly")
        self.supervisor_combo.pack(side="left", fill="x", expand=True)

        # Date Selection with validation
        date_frame = ttk.Frame(self.info_frame)
        date_frame.pack(fill="x", pady=5)
        ttk.Label(date_frame, text="📅 Date:").pack(side="left", padx=(0, 10))
        self.date_picker = DateEntry(date_frame, width=38, background='darkblue',
                                   foreground='white', borderwidth=2,
                                   mindate=datetime(2023, 1, 1),
                                   maxdate=datetime(2023, 12, 31))
        self.date_picker.pack(side="left", fill="x", expand=True)
        self.date_picker.bind("<<DateEntrySelected>>", self.validate_date)

    def create_eval_frame(self):
        self.eval_frame = ttk.LabelFrame(self.main_frame, text="Evaluation Details", padding=10)
        self.eval_frame.pack(fill="x", pady=(0, 15))

        # Score with validation
        score_frame = ttk.Frame(self.eval_frame)
        score_frame.pack(fill="x", pady=5)
        ttk.Label(score_frame, text="📊 Score (0-100):").pack(side="left", padx=(0, 10))
        self.score_var = tk.StringVar()
        self.score_entry = ttk.Entry(score_frame, textvariable=self.score_var, width=10)
        self.score_entry.pack(side="left")
        self.score_label = ttk.Label(score_frame, text="", foreground="red")
        self.score_label.pack(side="left", padx=(10, 0))
        
        # Score slider for visual input
        self.score_slider = ttk.Scale(score_frame, from_=0, to=100, orient="horizontal",
                                    command=self.on_slider_change)
        self.score_slider.pack(side="left", padx=(10, 0), fill="x", expand=True)
        
        self.score_var.trace('w', lambda *args: self.validate_score())

        # Comments with character count
        ttk.Label(self.eval_frame, text="💬 Evaluation Comments:").pack(anchor="w", pady=(5, 0))
        self.comments = tk.Text(self.eval_frame, height=6, width=50)
        self.comments.pack(fill="x", pady=5)
        
        # Character count label
        self.char_count_label = ttk.Label(self.eval_frame, text="0/500 characters")
        self.char_count_label.pack(anchor="e")
        
        # Bind text changes to character count update
        self.comments.bind('<KeyRelease>', self.update_char_count)

    def create_buttons(self):
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill="x", pady=(15, 0))

        # Undo button
        self.undo_btn = ttk.Button(buttons_frame, text="↩ Undo", command=self.undo)
        self.undo_btn.pack(side="left", padx=5)
        
        # Cancel button
        ttk.Button(buttons_frame, text="Cancel", command=self.confirm_close).pack(side="left", padx=5)
        
        # Save as Draft button
        ttk.Button(buttons_frame, text="Save Draft", command=self.save_draft).pack(side="left", padx=5)
        
        # Submit button
        self.submit_btn = ttk.Button(buttons_frame, text="Submit Evaluation", 
                                   command=self.submit, style="Accent.TButton")
        self.submit_btn.pack(side="right", padx=5)

    def create_instructions(self):
        instructions = """
        Instructions:
        1. Select a training report from the dropdown list
        2. Choose the supervising instructor
        3. Select the evaluation date (must be after report date)
        4. Enter a score between 0 and 100 (use slider or type)
        5. Provide detailed comments (minimum 50 characters)
        6. Click Submit to save the evaluation
        
        Keyboard Shortcuts:
        • Ctrl + S: Submit evaluation
        • Ctrl + Z: Undo last change
        • Esc: Cancel/Close
        """
        instruction_frame = ttk.LabelFrame(self.main_frame, text="How to Use", padding=10)
        instruction_frame.pack(fill="x", pady=(15, 0))
        ttk.Label(instruction_frame, text=instructions, justify="left").pack()

    def load_data(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            # Get reports with student names that haven't been evaluated
            cursor.execute("""
                SELECT tr.report_id, s.student_name, tr.report_date, s.student_id 
                FROM training_reports tr 
                JOIN students s ON tr.student_id = s.student_id
                WHERE tr.report_id NOT IN (SELECT report_id FROM evaluations)
                ORDER BY tr.report_date DESC
            """)
            self.reports = cursor.fetchall()
            self.report_combo['values'] = [f"{row[0]} - {row[1]} ({row[2]})" for row in self.reports]

            # Get supervisors with departments
            cursor.execute("""
                SELECT supervisor_id, supervisor_name, department 
                FROM internal_supervisors
                ORDER BY department, supervisor_name
            """)
            self.supervisors = cursor.fetchall()
            self.supervisor_combo['values'] = [f"{row[0]} - {row[1]} ({row[2]})" for row in self.supervisors]

            conn.close()
            
            # Try to load saved draft
            self.load_draft()
            
        except Exception as e:
            logging.error(f"Error loading data: {str(e)}")
            messagebox.showerror("Database Error", str(e))
            self.window.destroy()

    def validate_score(self, *args):
        try:
            score = float(self.score_var.get())
            if 0 <= score <= 100:
                self.score_label.config(text="✓", foreground="green")
                self.score_slider.set(score)
                return True
            else:
                self.score_label.config(text="Score must be between 0 and 100", foreground="red")
                return False
        except ValueError:
            if self.score_var.get() != "":  # Don't show error for empty field
                self.score_label.config(text="Please enter a valid number", foreground="red")
            return False

    def on_slider_change(self, value):
        try:
            score = int(float(value))
            self.score_var.set(str(score))
        except ValueError:
            pass

    def validate_date(self, event=None):
        if not self.report_combo.get():
            return False
            
        try:
            report = self.reports[self.report_combo.current()]
            report_date = report[2]
            if isinstance(report_date, str):
                report_date = datetime.strptime(report_date, '%Y-%m-%d').date()
            selected_date = self.date_picker.get_date()
            
            if selected_date < report_date:
                messagebox.showwarning("Invalid Date", 
                                     "Evaluation date cannot be earlier than the report date!")
                self.date_picker.set_date(report_date)
                return False
            return True
        except Exception as e:
            logging.error(f"Error validating date: {str(e)}")
            return False

    def update_char_count(self, event=None):
        count = len(self.comments.get("1.0", tk.END).strip())
        self.char_count_label.config(text=f"{count}/500 characters")
        if count < 50:
            self.char_count_label.config(foreground="red")
        else:
            self.char_count_label.config(foreground="green")

    def on_report_select(self, event=None):
        if not self.report_combo.get():
            return
            
        try:
            selected_index = self.report_combo.current()
            if selected_index >= 0:
                report = self.reports[selected_index]
                # تحديث معلومات الطالب
                self.student_info.config(
                    text=f"Student: {report[1]} (ID: {report[3]})"
                )
                # تعيين التاريخ
                if isinstance(report[2], datetime):
                    self.date_picker.set_date(report[2])
                else:
                    self.date_picker.set_date(datetime.strptime(str(report[2]), '%Y-%m-%d'))
        except Exception as e:
            logging.error(f"Error in report selection: {str(e)}")
            messagebox.showerror("Error", "Failed to load report details")

    def save_draft(self):
        draft_data = {
            'report': self.report_combo.get(),
            'supervisor': self.supervisor_combo.get(),
            'date': self.date_picker.get_date().strftime('%Y-%m-%d'),
            'score': self.score_var.get(),
            'comments': self.comments.get("1.0", tk.END).strip()
        }
        
        try:
            with open('evaluation_draft.json', 'w') as f:
                json.dump(draft_data, f)
            messagebox.showinfo("Success", "Draft saved successfully!")
        except Exception as e:
            logging.error(f"Error saving draft: {str(e)}")
            messagebox.showerror("Error", "Failed to save draft")

    def load_draft(self):
        try:
            with open('evaluation_draft.json', 'r') as f:
                draft_data = json.load(f)
                
            if messagebox.askyesno("Load Draft", "Would you like to load the saved draft?"):
                self.report_combo.set(draft_data['report'])
                self.supervisor_combo.set(draft_data['supervisor'])
                self.date_picker.set_date(datetime.strptime(draft_data['date'], '%Y-%m-%d'))
                self.score_var.set(draft_data['score'])
                self.comments.delete("1.0", tk.END)
                self.comments.insert("1.0", draft_data['comments'])
                
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.error(f"Error loading draft: {str(e)}")

    def validate_all(self):
        if not self.report_combo.get():
            messagebox.showwarning("Validation Error", "Please select a report")
            return False
        if not self.supervisor_combo.get():
            messagebox.showwarning("Validation Error", "Please select a supervisor")
            return False
        if not self.validate_score():
            messagebox.showwarning("Validation Error", "Please enter a valid score (0-100)")
            return False
        if not self.validate_date():
            return False
        
        comments = self.comments.get("1.0", tk.END).strip()
        if len(comments) < 50:
            messagebox.showwarning("Validation Error", 
                                 "Please enter at least 50 characters in the comments")
            return False
        if len(comments) > 500:
            messagebox.showwarning("Validation Error", 
                                 "Comments cannot exceed 500 characters")
            return False
            
        return True

    def submit(self, event=None):
        if not self.validate_all():
            return

        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            # Get next evaluation ID
            cursor.execute("SELECT MAX(evaluation_id) FROM evaluations")
            new_id = (cursor.fetchone()[0] or 0) + 1

            # Extract IDs from selections
            report_id = int(self.report_combo.get().split(' - ')[0])
            supervisor_id = int(self.supervisor_combo.get().split(' - ')[0])

            cursor.execute("""
                INSERT INTO evaluations (
                    evaluation_id, report_id, supervisor_id, 
                    evaluation_date, evaluation_score, evaluation_comments
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                new_id,
                report_id,
                supervisor_id,
                self.date_picker.get_date().strftime('%Y-%m-%d'),
                float(self.score_var.get()),
                self.comments.get("1.0", tk.END).strip()
            ))

            conn.commit()
            conn.close()

            # Delete draft if exists
            try:
                import os
                os.remove('evaluation_draft.json')
            except:
                pass

            messagebox.showinfo("Success", "Evaluation added successfully!")
            self.window.destroy()

        except Exception as e:
            logging.error(f"Error submitting evaluation: {str(e)}")
            messagebox.showerror("Error", f"Failed to save evaluation: {str(e)}")

    def undo(self, event=None):
        # Implement undo functionality
        pass

    def confirm_close(self, event=None):
        if self.has_unsaved_changes:
            if messagebox.askyesno("Confirm Close", 
                                 "You have unsaved changes. Do you want to save a draft before closing?"):
                self.save_draft()
        self.window.destroy()

def open_insert_evaluation_form():
    EvaluationForm()
