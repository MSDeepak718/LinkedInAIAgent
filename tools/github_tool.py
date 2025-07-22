import os 
from dotenv import load_dotenv
from github import Github, GithubException # type: ignore
from langchain.tools import tool

load_dotenv()

def get_github_client():
    github_path = os.getenv("GITHUB_PATH")
    if not github_path:
        raise ValueError("GITHUB_PATH environment variable not set")
    return Github(github_path)

@tool
def get_repo_readme(repo_name: str) -> str:
    """
    Fetches the README.md content from the specified GitHub repository.
    """
    print(f"--- Attempting to fetch README for repo: {repo_name} ---")
    try:
        g = get_github_client()
        repo = g.get_repo(repo_name)
        readme_content = repo.get_contents("README.md")
        decoded_content = readme_content.decoded_content.decode("utf-8")
        print(f"--- Successfully fetched README for {repo_name} ---")
        return decoded_content
    except GithubException as e:
        if e.status == 404:
            return f"Error: Repository '{repo_name}' not found."
        return f"An error occurred while accessing Github: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"