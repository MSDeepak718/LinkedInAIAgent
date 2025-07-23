import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from graph.workflow import build_graph
import requests

load_dotenv

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

def main():
    app = build_graph()
    
    print("\nWelcome to the LinkedIn AI Agent!")
    print("You can ask it to write a post on a topic or a GitHub repository.")
    print("Type 'exit' or 'quit' to end the session.")
    
    while True:
        user_input = input("\n> What would you like to post about? ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the agent. Goodbye!")
            break
        
        if not user_input.strip():
            continue
        
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
        }
        
        print("\n--- Generating Post ---")
        final_state = None
        for event in app.stream(initial_state, stream_mode="values"):
            final_state = event
            
        if final_state and "messages" in final_state and final_state["messages"]:
            final_post = final_state["messages"][-1].content   
            print("\n" + "="*50)
            print("--- Generated LinkedIn Post ---")
            print("="*50)
            print(final_post)
            print("="*50 + "\n")
            
            publish_choice = input("> Would you like to publish this post to LinkedIn? (y/n): ").lower()
            if publish_choice == 'y':
                post_to_linkedin(final_post)
            else:
                print("Post not published.")
        else:
            print("Sorry, I couldn't generate a post for that request.")


if __name__ == "__main__":
    main()
