# Main application entry point
import database
# Initialize the database
#database.init_db()
#logs few tasks for testing
#database.log_task_db("Finish project report", "work", "started")
#database.log_task_db("Morning workout", "health", "completed")
#database.log_task_db("Read AI research paper", "learning", "started")
#database.log_task_db("Log task: Write documentation for work", "work", "completed")

# Retrieve and print summary for today
#summary_today = database.get_summary_db("today")
#print("Today's Summary:", summary_today)

# Retrieve and print all tasks
print(database.view_all_tasks())

# Clear all tasks
#database.clear_all_tasks()
#print("All tasks cleared.")
