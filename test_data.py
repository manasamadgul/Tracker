import sqlite3
conn = sqlite3.connect('C:\\Users\\Workspace\\ProductivityTracker\\productivity_tracker.db')
print("SQLite's 'now':", conn.execute("SELECT DATE('now')").fetchone())
print("Tasks from today:", conn.execute("SELECT * FROM tasks WHERE DATE(timestamp) = DATE('now')").fetchall())
conn.close()
