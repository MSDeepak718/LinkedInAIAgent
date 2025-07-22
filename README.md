# 🤖 LinkedIn AI Agent

### An autonomous, multi-agent system leverages a sophisticated backend using **LangGraph** to orchestrate specialized AI agents, **Groq** for high-speed LLM inference and has access to the Github and Web Search to generate and schedule engaging LinkedIn posts.

## Features

* **Autonomous Content Generation**: Automatically creates high-quality LinkedIn posts based on predefined topics or your public GitHub repositories.
* **Multi-Agent Framework**: Built with LangGraph to create a robust workflow where specialized agents collaborate:
    * A **Research Agent** explores trending topics using the Tavily search API.
    * A **GitHub Agent** analyzes your project READMEs to draft posts about your work.
    * A **Writer Agent** refines the gathered information into a polished, ready-to-publish post.
* **Scheduled Posting**: Uses a built-in scheduler to trigger post generation at configurable intervals.
* **High-Speed LLM**: Powered by the Groq API (`llama3-70b-8192`) for exceptionally fast content generation.
* **Deployable API**: The entire application is wrapped in a FastAPI server, making it easy to deploy and monitor.

## Technology Stack

* **Orchestration**: LangGraph
* **Language Model**: Groq (Llama 3)
* **Backend Framework**: FastAPI
* **Web Search**: Tavily AI
* **Package Management**: UV

## Prerequisites

### System

* Python 3.10+
* UV (Python package manager)

### API Keys

Before you begin, you need to acquire the following API keys and add them to a `.env` file in the project root:

* **`GROQ_API_KEY`**: Get from the [Groq Console](https://console.groq.com/keys).
* **`TAVILY_API_KEY`**: Get from the [Tavily AI Dashboard](https://tavily.com/).
* **`GITHUB_PAT`**: Generate a Personal Access Token from your [GitHub Developer Settings](https://github.com/settings/tokens) with `repo` scope.

## Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone [https://github.com/your-username/linkedin-agent.git](https://github.com/your-username/linkedin-agent.git)
cd linkedin-agent
```

### 2️⃣ Create the Environment File

Create a file named .env in the root of the project and populate it with your API keys.

```bash
# .env file

GROQ_API_KEY="your_groq_api_key"
TAVILY_API_KEY="your_tavily_api_key"
GITHUB_PAT="your_github_personal_access_token"

# These are placeholders for when you integrate the real LinkedIn API
LINKEDIN_CLIENT_ID="your_linkedin_client_id"
LINKEDIN_CLIENT_SECRET="your_linkedin_client_secret"
LINKEDIN_ACCESS_TOKEN="your_linkedin_access_token"
LINKEDIN_AUTHOR_URN="your_linkedin_author_urn"
```

### 3️⃣ Setup Backend with uv

Create the virtual environment and install all required dependencies.

```bash
# Create the virtual environment
uv venv

# Activate the environment
# On Windows (PowerShell):
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```
### 4️⃣ Configure Your Content

Open the main.py file and update the following lists with your desired topics and GitHub repositories:

```bash
# main.py

TOPICS = [
    "Your first topic here",
    "Another interesting topic",
]

GITHUB_REPOS = [
    "your-github-username/your-first-repo",
    "your-github-username/your-second-repo",
]
```

### 5️⃣ Run the FastAPI Server

Start the application using uvicorn. The --reload flag enables hot-reloading for development.

```bash
uvicorn main:api --reload
```
The service will be available at http://127.0.0.1:8000. It will immediately run one content generation cycle upon startup and then follow the schedule defined in main.py (default is every single day).


