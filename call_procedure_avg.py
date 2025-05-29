import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db

def open_avg_score_form():
    window = tk.Toplevel()
    window.title("Get Student Average Score")
    window.geometry("400x300")
    window.configure(bg="#f5f5f7")

    # Center window
    window_width = 400
    window_height = 300
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Style
    style = ttk.Style()
    style.configure("TLabel", background="#f5f5f7", font=("Segoe UI", 10))
    style.configure("TEntry", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10, "bold"))

    # Main frame
    main_frame = ttk.Frame(window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title
    title_label = ttk.Label(main_frame, text="Get Student Average Score", font=("Segoe UI", 14, "bold"))
    title_label.pack(pady=(0, 20))

    # Student selection
    student_frame = ttk.Frame(main_frame)
    student_frame.pack(fill="x", pady=10)

    ttk.Label(student_frame, text="Select Student:").pack(side="left", padx=(0, 10))
    student_combo = ttk.Combobox(student_frame, width=30, state="readonly")
    student_combo.pack(side="left", fill="x", expand=True)

    # Load students
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, student_name FROM students ORDER BY student_name")
        students = cursor.fetchall()
        student_combo['values'] = [f"{row[0]} - {row[1]}" for row in students]
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load students: {e}")
        window.destroy()
        return

    def get_average():
        if not student_combo.get():
            messagebox.showwarning("Input Required", "Please select a student")
            return

        try:
            student_id = int(student_combo.get().split(' - ')[0])
            
            conn = connect_to_db()
            cursor = conn.cursor()

            # Get student's evaluations
            cursor.execute("""
                SELECT s.student_name, AVG(e.evaluation_score) as avg_score, COUNT(e.evaluation_id) as eval_count
                FROM students s
                LEFT JOIN training_reports tr ON s.student_id = tr.student_id
                LEFT JOIN evaluations e ON tr.report_id = e.report_id
                WHERE s.student_id = %s
                GROUP BY s.student_id, s.student_name
            """, (student_id,))
            
            result = cursor.fetchone()
            conn.close()

            if result and result[1] is not None:
                name, avg_score, eval_count = result
                messagebox.showinfo("Average Score", 
                    f"Student: {name}\n"
                    f"Average Score: {avg_score:.2f}\n"
                    f"Based on {eval_count} evaluation(s)")
            else:
                messagebox.showinfo("No Data", 
                    "No evaluations found for this student.\n"
                    "Please make sure the student has completed reports and evaluations.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate average: {e}")

    # Get Average button
    ttk.Button(main_frame, text="Calculate Average", command=get_average).pack(pady=20)

    # Instructions
    instructions = """
    Instructions:
    1. Select a student from the dropdown
    2. Click 'Calculate Average' to see their average evaluation score
    3. The average is calculated from all available evaluations
    """
    ttk.Label(main_frame, text=instructions, justify="left", wraplength=350).pack(pady=20)
