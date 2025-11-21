# LangChain agent logic
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from tools import log_task, get_summary

# Initialize the Ollama chat model# Initialize
llm = ChatOllama(model="llama3.2", temperature=0)
tools = [log_task, get_summary]
# Bind tools to the model
llm_with_tools = llm.bind_tools(tools)

# Test
if __name__ == "__main__":
    question = "How was my week?"
    messages = [
        SystemMessage(content="You are a helpful coach and analyst assistant."),
        HumanMessage(content=question)
    ]
    
    response = llm_with_tools.invoke(messages)
    print(response)

    if response.tool_calls:
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
    
    # Call the model again with tool results
    final_response = llm_with_tools.invoke(messages)
    print("\nFinal Answer:")
    print(final_response.content)
else:
    # Module was imported rather than executed as a script; there is no response to print.
    print("Agent module imported; run this file as a script to execute the agent and produce a response.")

