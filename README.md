# 🤖 LinkedIn AI Agent

An interactive, multi-agent system that leverages a sophisticated backend using **LangGraph** to orchestrate specialized AI agents, **Groq** for high-speed LLM inference, and has access to **GitHub** and **Web Search** to generate engaging LinkedIn posts based on user prompts.

---

## Features

-   **Interactive Content Generation**: Run the application from your command line and tell the agent exactly what you want to post about in real-time.
-   **Intelligent Multi-Agent Framework**: Built with LangGraph to create a robust workflow that intelligently routes your request to the best-specialized agent for the job:
    -   A **Research Agent** explores general topics using the Tavily search API.
    -   An **Upgraded GitHub Agent** analyzes project READMEs and can also perform web searches to gather additional context.
-   **Optional Direct Publishing**: After a post is generated, you have the option to instantly publish it to your LinkedIn profile using the official LinkedIn API.
-   **High-Speed LLM**: Powered by the Groq API (`llama3-70b-8192`) for exceptionally fast content generation.
-   **Command-Line Interface**: A clean and simple CLI for easy interaction.

---

## Technology Stack

-   **Orchestration**: LangGraph
-   **Language Model**: Groq (Llama 3)
-   **Web Search**: Tavily AI
-   **GitHub Integration**: PyGithub
-   **Package Management**: uv

---

## Prerequisites

### System

-   Python 3.10+
-   [uv](https://github.com/astral-sh/uv) (Python package manager)

### API Keys

Before you begin, you need to acquire the following API keys and add them to a `.env` file in the project root:

-   **`GROQ_API_KEY`**: Get from the [Groq Console](https://console.groq.com/keys).
-   **`TAVILY_API_KEY`**: Get from the [Tavily AI Dashboard](https://tavily.com/).
-   **`GITHUB_PAT`**: Generate a Personal Access Token from your [GitHub Developer Settings](https://github.com/settings/tokens) with `repo` scope.

---

## Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/MSDeepak718/LinkedInAIAgent.git
cd LinkedInAIAgent
```

### 2️⃣ Create the Environment File

Create a file named .env in the root of the project and populate it with your API keys. The LinkedIn keys are only required if you want to use the final publishing feature.


```bash
# .env file

# Required for content generation
GROQ_API_KEY="your_groq_api_key"
TAVILY_API_KEY="your_tavily_api_key"
GITHUB_PAT="your_github_personal_access_token"

# Optional: Add these only if you want to publish directly to LinkedIn
LINKEDIN_CLIENT_ID="your_linkedin_client_id"
LINKEDIN_CLIENT_SECRET="your_linkedin_client_secret"
LINKEDIN_ACCESS_TOKEN="your_linkedin_access_token"
LINKEDIN_AUTHOR_URN="your_linkedin_author_urn"
```
### 3️⃣ Setup Backend with uv

Create the virtual environment and install all required dependencies from requirements.txt.

```bash
# Create the virtual environment
uv venv

# Activate the environment
# On Windows (PowerShell):
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv sync
```

## Usage

###  You can run the application directly from your terminal.

### 1️⃣ Run the Application

Create the virtual environment and install all required dependencies from requirements.txt.

```bash
python main.py
```

### 2️⃣ Interact with the Agent

The application will start and prompt you for input.

```bash
Welcome to the LinkedIn AI Agent!
You can ask it to write a post on a topic or a GitHub repository.
Type 'exit' or 'quit' to end the session.

> What would you like to post about?
```

### 3️⃣ Publish the Post

After the agent generates the content, it will be displayed, and you will be asked if you want to publish it.

```bash
> Would you like to publish this post to LinkedIn? (y/n):
```
Enter y to post it directly to your profile, or n to skip publishing.













