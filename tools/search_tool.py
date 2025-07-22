import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch # type: ignore

load_dotenv()

def get_search_tool():
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY environment variable not set")
    search_tool = TavilySearch(max_results=5, api_key=tavily_api_key)
    return search_tool