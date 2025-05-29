import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from db_connection import connect_to_db

def open_upload_students():
    filepath = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    if not filepath:
        return

    try:
        df = pd.read_excel(filepath)

        required_columns = {'student_id', 'student_name', 'program', 'enrollment_year', 'cgpa'}
        if not required_columns.issubset(df.columns):
            messagebox.showerror("Invalid File", f"Excel file must contain columns: {', '.join(required_columns)}")
            return

        conn = connect_to_db()
        cursor = conn.cursor()

        inserted = 0
        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO students (student_id, student_name, program, enrollment_year, cgpa)
                    VALUES (%s, %s, %s, %s, %s)
                """, (int(row['student_id']), row['student_name'], row['program'], int(row['enrollment_year']), float(row['cgpa'])))
                inserted += 1
            except Exception as e:
                print(f"Skipping row due to error: {e}")

        conn.commit()
        conn.close()

        messagebox.showinfo("Upload Complete", f"Successfully inserted {inserted} student records.")

    except Exception as e:
        messagebox.showerror("Upload Failed", f"Error: {e}")
