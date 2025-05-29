# report_export.py

import pandas as pd
from tkinter import messagebox, filedialog
from db_connection import connect_to_db
import logging

def export_reports():
    try:
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Report As"
        )
        
        if not file_path:
            return
            
        conn = connect_to_db()
        cursor = conn.cursor()
        
        # Get all reports with related information
        query = """
            SELECT 
                s.student_id,
                s.student_name,
                o.organization_name,
                tr.report_date,
                tr.report_text,
                e.evaluation_score,
                e.evaluation_comments,
                CONCAT(sv.supervisor_name, ' (', sv.department, ')') as supervisor
            FROM students s
            JOIN training_reports tr ON s.student_id = tr.student_id
            JOIN organizations o ON tr.organization_id = o.organization_id
            LEFT JOIN evaluations e ON tr.report_id = e.report_id
            LEFT JOIN internal_supervisors sv ON e.supervisor_id = sv.supervisor_id
            ORDER BY tr.report_date DESC
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            messagebox.showinfo("No Data", "No reports found to export.")
            return
            
        columns = [
            'Student ID',
            'Student Name',
            'Organization',
            'Report Date',
            'Report Content',
            'Evaluation Score',
            'Evaluation Comments',
            'Supervisor'
        ]
        
        df = pd.DataFrame(rows, columns=columns)
        
        # Format dates
        df['Report Date'] = pd.to_datetime(df['Report Date']).dt.strftime('%Y-%m-%d')
        
        # Format scores to 2 decimal places
        df['Evaluation Score'] = df['Evaluation Score'].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "Not Evaluated")
        
        # Save to Excel with formatting
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Training Reports')
            
            # Auto-adjust columns width
            worksheet = writer.sheets['Training Reports']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                )
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
        
        messagebox.showinfo("Export Complete", f"Report successfully exported to:\n{file_path}")
        conn.close()
        
    except Exception as e:
        logging.error(f"Failed to export reports: {str(e)}")
        messagebox.showerror("Error", f"Failed to export reports: {str(e)}")
