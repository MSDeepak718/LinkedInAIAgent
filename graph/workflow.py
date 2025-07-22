import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq # type: ignore

from agents.search_agent import create_search_agent
from agents.github_agent import create_github_agent
from tools.search_tool import get_search_tool
from tools.github_tool import get_repo_readme

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]

tools = [get_search_tool(), get_repo_readme]
tool_node = ToolNode(tools)

search_agent = create_search_agent()
github_agent = create_github_agent()
writer_llm = ChatGroq(model="llama3-70b-8192", temperature=0.7, api_key=os.getenv("GROQ_API_KEY"))

def format_intermediate_steps(messages: list):
    intermediate_steps = []
    for i in range(len(messages) - 1):
        if isinstance(messages[i], AIMessage) and messages[i].tool_calls:
            if (i + 1 < len(messages)) and isinstance(messages[i+1], ToolMessage) and messages[i+1].tool_call_id == messages[i].tool_calls[0].id:
                intermediate_steps.append((messages[i], messages[i+1]))
    return intermediate_steps

def agent_node(state: AgentState, agent, name: str):
    print(f"--- Calling {name} Agent Node ---")
    intermediate_steps = format_intermediate_steps(state["messages"])
    agent_input = {
        "input": state["messages"][0].content,
        "intermediate_steps": intermediate_steps
    }
    result = agent.invoke(agent_input)
    if isinstance(result, list):
        message = result[0]
    else:
        message = result
    return {"messages": [message]}

def research_node(state: AgentState):
    return agent_node(state, search_agent, "Research")

def github_node(state: AgentState):
    return agent_node(state, github_agent, "GitHub")

def writer_node(state: AgentState):
    print("--- Calling Writer Node ---")
    last_msg = state["messages"][-1]
    print(f"DEBUG: Last message in state is of type: {type(state['messages'][-1])}")
    
    if hasattr(last_msg, "content"):
        summary = last_msg.content
    else:
        summary = str(last_msg)
    
    original_query = state["messages"][0].content
    
    prompt = f"""
    You are a professional content creator for LinkedIn. Your task is to take the following summary
    and the original request to transform it into an engaging and insightful LinkedIn post.
    **Original Request:** "{original_query}"
    **Summary to use:**\n---\n{summary}\n---
    **Instructions:**
    1.  **Hook:** Start with a strong opening that grabs attention.
    2.  **Body:** Expand on the key points from the summary. Add value by providing context or asking a thought-provoking question.
    3.  **Structure:** Use short paragraphs, bullet points, and emojis to make the post easy to read.
    4.  **Hashtags:** Include 3-5 relevant hashtags at the end.
    5.  **Tone:** Maintain a professional yet approachable tone.
    **Generated LinkedIn Post:**
    """
    
    response = writer_llm.invoke(prompt)
    print("--- Generated Post ---")
    print(response.content)
    return {"messages": [HumanMessage(content=response.content)]}

def router(state: AgentState):
    print("--- Routing ---")
    initial_input = state["messages"][0].content.lower()
    if "github.com" in initial_input or ("/" in initial_input and len(initial_input.split('/')) == 2):
        print("--- Route: GitHub ---")
        return "github"
    else:
        print("--- Route: Research ---")
        return "research"

def after_agent_router(state: AgentState):
    print("--- Deciding Next Step After Agent ---")
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    else:
        return "writer"

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("research", research_node)
    workflow.add_node("github", github_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("tools", tool_node)
    workflow.set_conditional_entry_point(router, {"research": "research", "github": "github"})
    workflow.add_conditional_edges("research", after_agent_router, {"tools": "tools", "writer": "writer"})
    workflow.add_conditional_edges("github", after_agent_router, {"tools": "tools", "writer": "writer"})
    workflow.add_edge("tools", "writer")
    workflow.add_edge("writer", END)
    app = workflow.compile()
    print("--- Graph Compiled ---")
    return app