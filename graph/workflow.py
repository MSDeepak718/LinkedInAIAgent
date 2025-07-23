from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq # type: ignore

from agents.search_agent import create_search_agent
from agents.github_agent import create_github_agent

from tools.search_tool import get_search_tool
from tools.github_tool import get_repo_readme

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    
tools = [get_search_tool(), get_repo_readme]
tool_node = ToolNode(tools)

search_agent = create_search_agent()
github_agent = create_github_agent()

def search_agent_node(state: AgentState):
    print("--- Calling Research Agent ---")
    result = search_agent.invoke(state)
    return {"messages": [result]}

def github_agent_node(state: AgentState):
    print("--- Calling Github Agent ---")
    result = github_agent.invoke(state)
    return {"messages":[result]}

def initial_router(state: AgentState) -> str:
    print("--- Routing Initial Agent ---")
    initial_input = state["messages"][0].content.lower()
    
    if "github" in initial_input or ("/" in initial_input and len(initial_input.split('/'))==2):
        print("--- Route: Github Agent ---")
        return "github_agent"
    else:
        print("--- Route: Research Agent ---")
        return "research_agent"
    
def after_agent_router(state: AgentState) -> str:
    print("--- Deciding Next Step ---")
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print("--- Decision: Agent called a tool, routing to tools ---")
        return "tools"
    else:
        print("--- Decision: Agent finished execution, ending graph ---")
        return END
    
def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("research_agent", search_agent_node)
    workflow.add_node("github_agent", github_agent_node)
    workflow.add_node("tools", tool_node)
    workflow.set_conditional_entry_point(
        initial_router,
        {
            "research_agent": "research_agent",
            "github_agent": "github_agent",
        }
    )
    
    workflow.add_conditional_edges("research_agent", after_agent_router, {"tools": "tools", END: END})
    workflow.add_conditional_edges("github_agent", after_agent_router, {"tools": "tools", END: END})
    workflow.add_edge("tools", "research_agent")
    
    app = workflow.compile()
    print("--- Graph is Compiled Successfully ---")
    return app