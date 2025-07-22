import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq # type: ignore
from langchain.agents import create_tool_calling_agent
from tools.search_tool import get_search_tool

load_dotenv()

def create_search_agent():
    print("--- Creating Research Agent (Modern) ---")
    tools = [get_search_tool()]

    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )
    

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
         You are an expert research analyst. Your mission is to provide the most
         accurate, relevant, and up-to-date information on a given topic.
         
         - Use your search tool to find information.
         - Synthesize the search results into a concise, easy-to-read summary.
         - Focus on key points, recent developments, and interesting facts.
         - If you have enough information to answer, provide the summary directly.
           Otherwise, you must call the search tool to get the information.
         """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"), 
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    
    print("--- Research Agent Created ---")
    return agent
