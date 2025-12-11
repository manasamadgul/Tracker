import sqlite3

conn = sqlite3.connect('productivity_tracker.db')
cursor = conn.cursor()

# Test query
cursor.execute("SELECT * FROM tasks")
results = cursor.fetchall()

for row in results:
    print(row)

conn.close()


"""
# Test query
cursor.execute("SELECT category, status, COUNT(*), GROUP_CONCAT(task_name, ', ') FROM tasks WHERE DATE(timestamp) = DATE('now') GROUP BY category, status")
results = cursor.fetchall()

for row in results:
    print(row)

conn.close()

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
"""