import schedule # type: ignore
import time
import random
import threading
import os
from dotenv import load_dotenv
import requests
from contextlib import asynccontextmanager
from fastapi import FastAPI # type: ignore
from uvicorn import run as uvicorn_run # type: ignore
from langgraph.graph import START
from langchain_core.messages import HumanMessage

from graph.workflow import build_graph

load_dotenv()

TOPICS = [
    "The future of AI in software development",
    "Latest trends in severless computing",
    "How LangGraph is changing multi-agent system development",
    "A deep dive into Retrieval-Augmented Generation (RAG)"
]

GITHUB_REPOS = [
    "MSDeepak718/Hygeia-Ragbot"
]

def post_to_linkedin(content: str):
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    author_urn = os.getenv("LINKEDIN_AUTHOR_URN")
    
    if not access_token or not author_urn:
        return "Error: Missing LinkedIn Credentials."

    api_url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    try:
        print("--- Attempting to post on LinkedIn")
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        print("-- Post successfully published ---")
    except requests.exceptions.HTTPError as e:
        print(f"Response Body: {e.response.text}")
        return f"Error: {e.response.text}"
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return f"An unexpected error occured: {e}"

def trigger_post_generation():
    
    print(f"\n{'='*20} Triggering New Post Generation {'='*20}")
    app = build_graph()
    
    if random.random() > 0.5 and GITHUB_REPOS:
        content_source = random.choice(GITHUB_REPOS)
        print(f"Chosen Content Source: Github Repo - {content_source}")
    else:
        content_source = random.choice(TOPICS)
        print(f"Chosen Content Source: Topic - {content_source}")
        
    initial_state = {
        "messages": [HumanMessage(content=content_source)]
    }    
    final_state = None
    for event in app.stream(initial_state, stream_mode="values"):
        final_state = event
    
    if final_state and "messages" in final_state and final_state["messages"]:
        final_post = final_state["messages"][-1].content
        post_to_linkedin(final_post)
    else:
        print("Error: Could not generate post content.")
        
    print(f"{'='*20} Post Generation Cycle Complete {"="*20}\n")

def run_scheduler():
    schedule.every(1440).minutes.do(trigger_post_generation)
    print("Scheduler started. Waiting for the first job...")
    while True:
        schedule.run_pending()
        time.sleep(1)
        
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for the FastAPI application
    """
    print("--- Application Startup ---")
    threading.Thread(target=trigger_post_generation, daemon=True).start()
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    print("--- Scheduler has been started in the background ---")
    yield
    print("--- Application Shutdown ---")
        
api = FastAPI(
    lifespan = lifespan,
    title = "LinkedIn AI Agent",
    description = "An AI Agent for autonomously generating linkedin posts.",
    version = "1.0.0",
)

@api.get("/", tags=["Monitoring"])
def read_root():
    """
    Root endpoint to check if the service is running.
    """
    return {"status": "LinkedIn Agent is running"}

if __name__ == "__main__":
    print("Starting FastAPI Server...")
    uvicorn_run(api, host="0.0.0.0", port=8000)

    