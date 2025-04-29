import sys, logging, os
from contextlib import redirect_stdout
from mcp.server.fastmcp import FastMCP
from edapi import EdAPI

# Initialize MCP server with a clear name
mcp = FastMCP("Ed Discussion MCP Server")
ed = EdAPI()

# Check for API token in environment variable
if 'ED_API_TOKEN' in os.environ:
    ed.api_token = os.environ['ED_API_TOKEN']
    print("API token loaded from environment variable")
# Fallback to command line argument if provided
elif len(sys.argv) > 1:
    ed.api_token = sys.argv[1]
    print("API token loaded from command line argument")
else:
    logging.error("ED_API_TOKEN not provided in environment or as command line argument")
    sys.exit(1)

logging.info("Ed Discussion MCP Server ready.")

@mcp.tool()
def fetch_ed_posts(course_id: int, category: str = "General") -> list:
    """
    Fetch relevant Ed Discussion posts given a user question.
    """ 
    threads = ed.list_threads(course_id, limit=50)
    return threads

@mcp.tool()
def craft_ed_question(title: str, content: str, category: str = "General", anonymous: bool = False, isPrivate: bool = False) -> dict:
    """
    Craft a new question for Ed Discussion without posting it.
    Returns a preview that the user should review and approve before posting.
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
            "is_private": isPrivate,
            "is_anonymous": anonymous,
            "is_megathread": False,
            "anonymous_comments": False
        }
    return {
        "status": "preview",
        "message": "Question crafted successfully. Review before posting.",
        "post_data": params,
        "preview": {
            "title": title,
            "content": content,
            "category": category,
            "is_anonymous": anonymous,
            "is_private": isPrivate
        }
    }

@mcp.tool()
def submit_ed_question(course_id: int, post_data: dict) -> dict:
    """
    Submit a previously crafted question to Ed Discussion.
    This should only be used after the user has reviewed a question created with craft_ed_question and approved it.
    """
    result = ed.post_thread(course_id, post_data)
    return {"status": "success", "message": "Question posted successfully", "result": result}

@mcp.tool()
def get_user_info() -> dict:
    """Get info about the currently authenticated Ed Discussion user."""
    # Get the user info from EdAPI
    user_info = ed.get_user_info()
        
    return user_info

@mcp.tool()
def get_thread(thread_id: int) -> dict:
    """Get details for a specific Ed Discussion thread by thread ID."""
    return ed.get_thread(thread_id)

@mcp.tool()
def list_user_activity(user_id: int, course_id: int, limit: int = 20, filter: str = "all") -> list:
    """List a user's activity (threads/comments) in a course."""
    return ed.list_user_activity(user_id, course_id, limit=limit, filter=filter)

@mcp.tool()
def upload_file(filename: str, content_type: str) -> dict:
    """Upload a file to Ed Discussion. Provide the local filename and its content type (e.g., 'image/png')."""
    return ed.upload_file(filename, content_type)

@mcp.tool()
def find_course_id(course_name: str) -> dict:
    """
    Find a course ID by its name or code (e.g., 'CS 3410').
    Searches through the user's enrolled courses and returns the matching course ID.
    """
    user_info = ed.get_user_info()
    matches = []
    
    # Normalize input for matching
    course_name_lower = course_name.lower().strip()
    
    for course in user_info["courses"]:
        # Check for matches in course code or name
        if (course_name_lower in course["course"]["code"].lower() or 
            course_name_lower in course["course"]["name"].lower()):
            matches.append({
                "id": course["course"]["id"],
                "code": course["course"]["code"],
                "name": course["course"]["name"]
            })
    
    if not matches:
        return {"status": "error", "message": f"No course matching '{course_name}' found"}
    elif len(matches) == 1:
        return {"status": "success", "course": matches[0]}
    else:
        return {"status": "multiple_matches", "matches": matches}

if __name__ == "__main__":
    mcp.run(transport="stdio")    