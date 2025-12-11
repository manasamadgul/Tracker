# Tool functions (log_task, get_summary, etc.)
#log_task(task_name, category, status) - This should accept a task name, category (work/health/learning), and status (started/completed).
from enum import Enum
from langchain.tools import tool
from typing import Optional
import database

class Category(Enum):
    WORK = "work"
    HEALTH = "health"
    LEARNING = "learning"
    PERSONAL = "personal"
    FINANCE = "finance"
    SOCIAL = "social"
    HOBBY = "hobby"
    SELF_CARE = "self_care"

class Status(Enum):
    TODO = "todo"
    BLOCKED = "blocked"
    STARTED = "started"
    COMPLETED = "completed"

@tool
def log_task(task_name: str, category: str, status: str):
    """
    Log a new task with its category and current status.

    Use this tool when the user wants to record or track a task they're working on or planning to do.

    Common phrases that should use this tool:
    - "Log a task..."
    - "Add a task..."
    - "I'm starting/working on..."
    - "Track this task..."

    Args:
        task_name: Name or description of the task
        category: Type of task
            - work: Professional tasks, meetings, projects, deadlines
            - health: Exercise, medical appointments, nutrition, wellness
            - learning: Study, courses, reading, skill development
            - personal: Errands, household chores, organization
            - finance: Budgeting, bills, expenses, financial planning
            - social: Time with friends, family interactions, social events
            - hobby: Creative projects, recreational activities, entertainment
            - self_care: Meditation, journaling, relaxation, personal growth
        status: Current state - todo (planned), started (in progress), completed (finished), blocked (waiting on something)

    Returns:
        Confirmation message with task details

    Examples:
        - Log workout task: category=health, status=completed
        - Log code review: category=work, status=started
        - Log bill payment: category=finance, status=todo
"""

    # Implementation to log the task
    try:

        category_enum = next(c for c in Category if c.value == category.lower())
        status_enum = next(s for s in Status if s.value == status.lower())
        print(f"Converting: {category} -> {category_enum}, {status} -> {status_enum}")
        database.log_task_db(task_name, category_enum.value, status_enum.value)
        return f"Task '{task_name}' logged under category '{category_enum.value}' with status '{status_enum.value}'."
    except Exception as e:
        return f"Error logging task: {str(e)}"

@tool
def get_summary(period: str):
    """
    Retrieve a summary of logged tasks for a specific time period.

    Use this tool when the user asks about their progress, productivity, or wants to see what they've accomplished.

    Common questions that should use this tool:
    - "How is my day/week/month going?"
    - "What have I done today?"
    - "Show me my progress"
    - "What tasks did I complete?"

    Args:
    period: Time period to summarize - "today", "week", or "month"

    Returns:
    Dictionary with task counts by category and status
    """
  
    # Implementation to get the summary
    summary = database.get_summary_db(period)
    return f"Summary for {period}: summary: {summary}"

@tool
def update_task_status(task_id: Optional[int] = None, task_name: Optional[str] = None, new_status: str = None):
    """
    Update the status of an existing task.

    Use this tool when the user wants to change the status of a task they have already logged.

    Common phrases that should use this tool:
    - "Update task status..."
    - "Change status of..."
    - "Mark task as..."
    - "Set task to..."

    Args:
        task_id: Unique identifier of the task (optional if task_name is provided)
        task_name: Name or description of the task (optional if task_id is provided)
        new_status: New status to set - todo (planned), started (in progress), completed (finished), blocked (waiting on something)

    Returns:
        Confirmation message with updated task details
    """
    new_status_enum = next(s for s in Status if s.value == new_status.lower())

    if not new_status_enum or (not task_id and not task_name):
        return "Must provide new_status and either task_id or task_name."
    
    # Implementation to update the task status
    try:
        result = database.update_task_status_db(task_id, task_name, new_status_enum.value)
        return result
    except Exception as e:
        return f"Error logging task: {str(e)}"

@tool
def remove_task(task_id: Optional[int] = None, task_name: Optional[str] = None):
    """
    Remove an existing task from the database.

    Use this tool when the user wants to delete a task they have logged.

    Common phrases that should use this tool:
    - "Remove task..."
    - "Delete task..."
    - "Clear task..."
    - "Erase task..."
    - "remove duplicate tasks..."

    Args:
        task_id: Unique identifier of the task (optional if task_name is provided)
        task_name: Name or description of the task (optional if task_id is provided)

    Returns:
        Confirmation message with details of the removed task
    """
    if not task_id and not task_name:
        return "Must provide either task_id or task_name to remove a task."
    
    # Implementation to remove the task
    result = database.remove_task_db(task_id, task_name)
    return result