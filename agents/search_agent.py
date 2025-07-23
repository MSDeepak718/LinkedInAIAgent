import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq # type: ignore
from tools.search_tool import get_search_tool

load_dotenv()

def create_search_agent():
    print("--- Creating Research Agent (Modern) ---")
    tools = [get_search_tool()]

    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )
    

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an expert research analyst and content creator for LinkedIn.
        Your mission is to answer a user's query by searching the web for the
        most accurate and up-to-date information.

        - Use your search tool to find information on the requested topic.
        - After gathering the information, synthesize it into a concise,
          engaging, and insightful LinkedIn post.
        
        IMPORTANT: Your final output MUST be only the text of the LinkedIn post itself.
        Do not include any introductory phrases, conversational text, or explanations
        like "Here is the post:".
        """),
        ("placeholder", "{messages}"),
    ])

    agent = prompt | llm.bind_tools(tools)
    
    print("--- Research Agent Created ---")
    return agent
