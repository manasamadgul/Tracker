from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel import NotificationOptions
import mcp.server.stdio
import mcp.types as types
import database
from tools import log_task, get_summary, update_task_status, remove_task

#MCP server for Productivity Tracker
server = Server("productivity-tracker")
database.init_db()

#Telling MCP clients that the log_task tool exists
@server.list_tools()
async def handle_list_tools() ->list[types.Tool]:
    return [
        types.Tool(
            name="log_task",
            description="Log a new task with category and status",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_name": {"type": "string"},
                    "category": {"type": "string"},
                    "status": {"type": "string"}
                },
                "required": ["task_name", "category", "status"]
            }
        ),
        types.Tool(
            name="get_summary",
            description="Get summary of tasks for a time period (today, week, month)",
            inputSchema={
                "type": "object",
                "properties": {
                    "period": {"type": "string"}
                },
                "required": ["period"]
            }
        ),
        types.Tool(
            name="update_task_status",
            description="Update the status of an existing task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"},
                    "task_name": {"type": "string"},
                    "new_status": {"type": "string"}
                },
                "required": ["new_status"]
            }
        ),
        types.Tool(
            name="remove_task",
            description="Remove a task by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"},
                    "task_name": {"type": "string"}
                },
                "required": []
            }
        )
    ]

#handle what happens when a client actually CALLS the tool
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "log_task":
        print(f"Received log_task with args: {arguments}")
        result = log_task.invoke(arguments)
        print(f"Result: {result}")
        return [types.TextContent(type="text", text=str(result))]
    elif name == "get_summary":
        result = get_summary.invoke(arguments)
        return [types.TextContent(type="text", text=str(result))]
    elif name == "update_task_status":
        result = update_task_status.invoke(arguments)
        return [types.TextContent(type="text", text=str(result))]
    elif name == "remove_task":
        result = remove_task.invoke(arguments)
        return [types.TextContent(type="text", text=str(result))]

#main entry point to run the MCP server.This sets up the server to communicate via stdio (standard input/output).
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="productivity-tracker",
            server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={})
        )
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

