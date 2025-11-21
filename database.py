# Data storage
import sqlite3
from datetime import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect('productivity_tracker.db')
    # Create tasks table if it doesn't exist
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (task_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                     task_name TEXT NOT NULL,
                     category TEXT NOT NULL,
                     status TEXT NOT NULL,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Log a new task
def log_task_db(task_name, category, status):
    conn = sqlite3.connect('productivity_tracker.db')
    conn.execute('INSERT INTO tasks (task_name, category, status) VALUES (?, ?, ?)',
                 (task_name, category, status))
    conn.commit()
    conn.close()
    
# Retrieve summary of tasks
def get_summary_db(period):
    conn = sqlite3.connect('productivity_tracker.db')
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
    
    cursor.execute(f'SELECT category, status, COUNT(*) FROM tasks WHERE {time_filter} GROUP BY category, status')
    results = cursor.fetchall()
    
    summary = {}
    for category, status, count in results:
        if category not in summary:
            summary[category] = {}
        summary[category][status] = count
    
    conn.close()
    return summary