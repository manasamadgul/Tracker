# Tool functions (log_task, get_summary, etc.)
#log_task(task_name, category, status) - This should accept a task name, category (work/health/learning), and status (started/completed).
from enum import Enum
from langchain.tools import tool
import database

class Category(Enum):
    WORK = "work"
    HEALTH = "health"
    LEARNING = "learning"

class Status(Enum):
    STARTED = "started"
    COMPLETED = "completed"

@tool
def log_task(task_name: str, category: Category, status: Status):
    """    
    Log a new task with its category and current status.
    Use this when the user wants to track a task they're working on.

    Args:
        task_name: Name or description of the task
        category: Type of task (work, health, or learning)
        status: Current state (started or completed)

    """ 
    # Implementation to log the task
    database.log_task_db(task_name, category.value, status.value)
    return f"Task '{task_name}' logged under category '{category.value}' with status '{status.value}'."

@tool
def get_summary(period: str):
    """  
    period could be "today", "week", "month"
  
    Retrieve a summary of logged tasks, categorized by type and status.
    Use this to get an overview of all tracked tasks for a particular period.

    Returns:
        A summary string of tasks.
    """    
    # Implementation to get the summary
    summary = database.get_summary_db(period)
    return f"Summary for {period}: summary: {summary}"