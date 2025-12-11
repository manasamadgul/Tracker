# LLM-Driven Productivity Tracker with MCP Integration

An intelligent task management system powered by LangChain agents and Model Context Protocol (MCP), enabling natural language interaction for productivity tracking.

## Features

- **Multi-step AI Agent**: Autonomous decision-making with LangChain for complex task workflows
- **Natural Language Interface**: Interact with your tasks using conversational AI
- **MCP Server Integration**: Exposes productivity tools via standardized protocol
- **Claude Desktop Compatible**: Works seamlessly as an MCP client
- **Comprehensive Task Management**: 
  - Log tasks with 8 categories (work, health, learning, personal, finance, social, hobby, self_care)
  - 4 status types (todo, started, completed, blocked)
  - Update and remove tasks by ID or name
  - Time-based summaries (daily, weekly, monthly)
- **Local LLM Support**: Runs on Ollama with llama3.2 (no API costs)

## Technologies

- Python 3.12
- LangChain (Agent framework)
- Ollama (llama3.2)
- Model Context Protocol (MCP)
- SQLite (Database)
- Claude Desktop API
- JSON-RPC

## Prerequisites

- Python 3.12+
- Ollama installed with llama3.2 model
- Claude Desktop (optional, for MCP integration)

## Installation

1. Clone the repository:
git clone cd ProductivityTracker


2. Install dependencies:
pip install -r requirements.txt


3. Install Ollama and pull llama3.2:
ollama pull llama3.2


4. Initialize the database:
python -c "import database; database.init_db()"


## Usage

### Option 1: Local Agent (agent.py)

Run the agent locally with your own questions:

python agent.py


Modify the `question` variable in `agent.py` to test different queries.

### Option 2: MCP Server with Claude Desktop

1. Configure Claude Desktop by editing `%APPDATA%\Claude\claude_desktop_config.json`:

{ "mcpServers": { "productivity-tracker": { "command": "C:\path\to\python.exe", "args": ["C:\path\to\ProductivityTracker\mcp_server.py"] } } }


2. Restart Claude Desktop

3. Interact naturally:
   - "Log a task to review code for work as started"
   - "Show me today's summary"
   - "Update test task to completed"

## Project Structure

ProductivityTracker/ ├── agent.py # Local LangChain agent with multi-step reasoning ├── mcp_server.py # MCP server exposing tools via protocol ├── tools.py # Tool definitions (log_task, get_summary, etc.) ├── database.py # SQLite operations with error handling ├── requirements.txt # Python dependencies └── productivity_tracker.db # SQLite database (auto-created)


## Example Interactions

**Log a task:**
"Log a morning workout for health category as completed"


**Get summary:**
"How was my week?"


**Update task:**
"Mark the code review task as completed"


**Remove task:**
"Delete the duplicate dinner task"


## Architecture

- **Agent Pattern**: AI decides which tools to use based on user intent
- **Tool Pattern**: 5 custom tools for task management operations
- **MCP Integration**: Standardized protocol for external agent communication
- **Iterative Loop**: Multi-step reasoning with context maintenance

## Error Handling

- Database connection errors handled gracefully
- Invalid category/status inputs caught with helpful messages