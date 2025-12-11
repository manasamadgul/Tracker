# Data storage
import sqlite3
from datetime import datetime
import os

DB_PATH = 'C:\\Users\\Workspace\\ProductivityTracker\\productivity_tracker.db'

def get_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file not found: {DB_PATH}")
    return sqlite3.connect(DB_PATH)

# Initialize database
def init_db():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)  # Creates file if missing
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (task_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                         task_name TEXT NOT NULL,
                         category TEXT NOT NULL,
                         status TEXT NOT NULL,
                         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        return "Database initialized successfully."
    except sqlite3.Error as e:
        return f"Database initialization error: {str(e)}"
    finally:
        if conn:
            conn.close()

def view_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def clear_all_tasks():
    conn = get_connection()
    conn.execute('DELETE FROM tasks')
    conn.commit()
    conn.close()

# Log a new task
def log_task_db(task_name, category, status):

    conn = None
    try:
        conn = get_connection()
        conn.execute('INSERT INTO tasks (task_name, category, status) VALUES (?, ?, ?)',
                    (task_name, category, status))
        conn.commit()
        return "Task logged successfully."
    except (sqlite3.Error, FileNotFoundError) as e:
        return f"Database error: {str(e)}. Please check database connection."
    finally:
        if conn:
            conn.close()    
    
# Retrieve summary of tasks
def get_summary_db(period):

    conn =None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Determine time range based on period
        if period == "today":
            time_filter = "DATE(timestamp) = DATE('now')"
        elif period == "week":
            time_filter = "timestamp >= DATE('now', '-7 days')"
        elif period == "month":
            time_filter = "timestamp >= DATE('now', '-1 month')"
        else:
            return "Invalid period specified."
        
        cursor.execute(f"SELECT category, status, COUNT(*), GROUP_CONCAT(task_name, ', ') FROM tasks WHERE {time_filter} GROUP BY category, status")
        #cursor.execute(f'SELECT category, status, COUNT(*) FROM tasks WHERE {time_filter} GROUP BY category, status')
        results = cursor.fetchall()
        
        summary = {}
        for category, status, count,task_name in results:
            if category not in summary:
                summary[category] = {}
            summary[category][status] = {'count':count, 'tasks': task_name.split(', ') if task_name else []}
        return summary
    except (sqlite3.Error, FileNotFoundError) as e:
        return f"Database error: {str(e)}. Please check database connection."
    finally:
        if conn:
            conn.close()

# Update task status based on task_id or task_name
def update_task_status_db(task_id=None, task_name=None, new_status=None):
    if not new_status or (not task_id and not task_name):
        return "Must provide new_status and either task_id or task_name."
    conn =None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if task_id:
            cursor.execute('UPDATE tasks SET status = ? WHERE task_id = ?', (new_status, task_id))
        else:
            cursor.execute('UPDATE tasks SET status = ? WHERE task_name like ?', (new_status, f'%{task_name}%'))
        
        conn.commit()
        return "Task status updated."
    except (sqlite3.Error, FileNotFoundError) as e:
        return f"Database error: {str(e)}. Please check database connection."
    finally:
        if conn:
            conn.close()

#remove duplicate tasks and unwanted tasks based on task_name or task_id
def remove_task_db(task_id=None, task_name=None):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if task_id:
            cursor.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
        elif task_name:
            cursor.execute('DELETE FROM tasks WHERE task_name like ?', (f'%{task_name}%',))
        else:
            return "Must provide either task_id or task_name to remove a task."
        
        conn.commit()
        return "Task(s) removed."
    except (sqlite3.Error, FileNotFoundError) as e:
        return f"Database error: {str(e)}. Please check database connection."
    finally:
        if conn:
            conn.close()
    