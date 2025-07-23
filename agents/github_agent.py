import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq # type: ignore
from langchain.agents import create_tool_calling_agent
from tools.github_tool import get_repo_readme
from tools.search_tool import get_search_tool

load_dotenv()

def create_github_agent():
    
    print("--- Creating Github Agent ---")
    
    llm = ChatGroq(
        model = "llama3-70b-8192",
        temperature = 0,
        api_key = os.getenv("GROQ_API_KEY")
    )
    
    tools = [get_repo_readme, get_search_tool]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an expert tech content writer specializing in creating engaging
        LinkedIn posts about software projects.

        You have access to two tools:
        1.  `get_repo_readme`: To fetch the README file from a GitHub repository.
        2.  `tavily_search_results_json`: To perform a web search for additional context.

        Your process is as follows:
        1.  You will be given a user's request, likely about a GitHub repository.
        2.  First, ALWAYS use the `get_repo_readme` tool to get the project's primary information.
        3.  After analyzing the README, if the user's request implies a need for more
            information (e.g., "write about its impact on the industry", "compare it to
            other tools"), use the `tavily_search_results_json` tool to find that context.
        4.  Once you have all the necessary information, synthesize it and write a
            complete, polished, and engaging LinkedIn post.
        
        IMPORTANT: Your final output MUST be only the text of the LinkedIn post itself.
        Do not include any introductory phrases, conversational text, or explanations
        like "Here is the post:".
        """),
        ("placeholder", "{messages}"),
    ])
    
    agent = prompt | llm.bind_tools(tools)
    
    print("--- GitHub Agent Created ---")
    return agent
    