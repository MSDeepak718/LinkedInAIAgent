import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq # type: ignore
from langchain.agents import create_tool_calling_agent
from tools.github_tool import get_repo_readme

load_dotenv()

def create_github_agent():
    
    print("--- Creating Github Agent ---")
    
    llm = ChatGroq(
        model = "llama3-8b-8192",
        temperature = 0,
        api_key = os.getenv("GROQ_API_KEY")
    )
    
    tools = [get_repo_readme]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
         You are an expert tech content writer. Your specialty is creating engaging
         summaries of software projects for professional platforms like LinkedIn.
         
         - You will be given the name of a GitHub repository.
         - Use your `get_repo_readme` tool to fetch its README file.
         - Analyze the README to understand the project's purpose, key features,
           and technology stack.
         - Summarize this information clearly and concisely. The summary should be
           ready to be used as the basis for a LinkedIn post.
         """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    print("--- GitHub Agent Created ---")
    return agent
    