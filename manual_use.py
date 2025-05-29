import tkinter as tk
from tkinter import scrolledtext

def open_manual_use():
    window = tk.Toplevel()
    window.title("Manual - How to Use Upload Feature")
    window.geometry("600x400")

    instructions = """
📤 How to Use 'Upload Students':

1. Prepare an Excel file (.xlsx or .xls) with the following columns:
   - student_id
   - student_name
   - program
   - enrollment_year
   - cgpa

2. Make sure all column names are spelled exactly like above.

3. From the dashboard, click 📤 Upload Students.

4. Select your Excel file from your device.

5. The system will:
   - Read the data
   - Validate columns
   - Insert each valid student into the database

✅ A success message will appear if all is good.
⚠️ Invalid rows will be skipped, and you’ll see the errors printed in the terminal.
    """

    text_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Segoe UI", 10))
    text_box.insert(tk.END, instructions)
    text_box.config(state=tk.DISABLED)
    text_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

