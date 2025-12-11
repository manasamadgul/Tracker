# LangChain agent logic
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from tools import log_task, get_summary, update_task_status, remove_task

# Initialize the Ollama chat model# Initialize
llm = ChatOllama(model="llama3.2", temperature=0)
tools = [log_task, get_summary, update_task_status, remove_task]
# Bind tools to the model
llm_with_tools = llm.bind_tools(tools)

# Test
if __name__ == "__main__":
    question = "Show me incomplete tasks from this week and log a new follow-up task"
    messages = [
        SystemMessage(content="You are a productivity tracking assistant and coach. You help users analyze their tasks, track progress, and improve efficiency. Always use the available tools to get real data - never make assumptions about what tasks exist or their status. Always include all categories, When showing summaries, always list the actual task names, not just counts and provide actionable insights based on the actual data.If tools return empty data or no results, clearly state that no tasks were found - never invent or assume tasks exist"),
        HumanMessage(content=question)
    ]
    
    response = llm_with_tools.invoke(messages)
    print(response)
#while loop to handle multiple tool calls

    while response.tool_calls:
        for call in response.tool_calls:
            tool_name = call['name']
            tool_args = call['args']
        
        # Find and execute the matching tool
            for tool in tools:
                if tool.name == tool_name:
                    tool_response = tool.invoke(tool_args)
                    print(f"Tool '{tool_name}' executed with result: {tool_response}")
        
        # Add tool result to messages
        from langchain_core.messages import ToolMessage
        messages.append(ToolMessage(
            content=str(tool_response),
            tool_call_id=call['id']
        ))
        # Get new response from the model - multiple tool calls possible
        response = llm_with_tools.invoke(messages)
    
    final_response = response
    print(final_response.content)
else:
    # Module was imported rather than executed as a script; there is no response to print.
    print("Agent module imported; run this file as a script to execute the agent and produce a response.")

