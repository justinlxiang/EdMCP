import sys, logging, os
from contextlib import redirect_stdout
from mcp.server.fastmcp import FastMCP
from edapi import EdAPI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize MCP server with a clear name
mcp = FastMCP("Ed Discussion MCP Server")
ed = EdAPI()
ed.api_token = str(os.environ.get("ED_API_TOKEN"))

logging.info("Ed Discussion MCP Server ready.")

print("HI")
@mcp.tool()
def fetch_ed_posts(course_id: int, question: str, category: str = "General") -> list:
    """
    Fetch relevant Ed Discussion posts given a user question.
    """ 
    threads = ed.list_threads(course_id, limit=20)
    matches = [t for t in threads if question.lower() in t['title'].lower()]
    return matches

@mcp.tool()
def post_ed_question(course_id: int, title: str, content: str, category: str = "General") -> dict:
    """
    Post a new question to Ed Discussion.
    """
    content_xml = f'<document version="2.0"><paragraph>{content}</paragraph></document>'
    params = {
            "type": "post",
            "title": title,
            "category": category,
            "subcategory": "",
            "subsubcategory": "",
            "content": content_xml,
            "is_pinned": False,
            "is_private": False,
            "is_anonymous": False,
            "is_megathread": False,
            "anonymous_comments": False
        }
    result = ed.post_thread(course_id, params)
    return {"result": result}

@mcp.tool()
def get_user_info() -> dict:
    """Get info about the currently authenticated Ed Discussion user."""
    # Get the user info from EdAPI
    user_info = ed.get_user_info()
    
    # Extract essential user data for a cleaner response
    simplified_info = {
        "user": {
            "id": user_info["user"]["id"],
            "name": user_info["user"]["name"],
            "email": user_info["user"]["email"],
            "role": user_info["user"]["role"]
        },
        "courses": [
            {
                "id": course["course"]["id"],
                "code": course["course"]["code"],
                "name": course["course"]["name"],
                "role": course["role"]["role"]
            }
            for course in user_info["courses"][:5]  # Limit to 5 courses for readability
        ]
    }
        
    return simplified_info

@mcp.tool()
def get_thread(thread_id: int) -> dict:
    """Get details for a specific Ed Discussion thread by thread ID."""
    return ed.get_thread(thread_id)

@mcp.tool()
def list_user_activity(user_id: int, course_id: int, limit: int = 10, filter: str = "all") -> list:
    """List a user's activity (threads/comments) in a course."""
    return ed.list_user_activity(user_id, course_id, limit=limit, filter=filter)

@mcp.tool()
def upload_file(filename: str, content_type: str) -> dict:
    """Upload a file to Ed Discussion. Provide the local filename and its content type (e.g., 'image/png')."""
    return ed.upload_file(filename, content_type)

if __name__ == "__main__":
    mcp.run()    