from mcp.server.fastmcp import FastMCP
from ed_client import EdClient

mcp = FastMCP("Ed Discussion MCP Server")
ed = EdClient()

@mcp.tool()
def set_api_token(token: str) -> str:
    """Set and save your Ed Discussion API token."""
    ed.set_api_token(token)
    return "API token saved successfully. You can now use Ed Discussion tools."

@mcp.tool()
def fetch_ed_posts(course_id: int, question: str, category: str = "General") -> list:
    """
    Fetch relevant Ed Discussion posts given a user question.
    """
    if not ed.api.api_token:
        return ["Please provide your Ed Discussion API token to continue."]
    threads = ed.get_threads(course_id, limit=20)
    matches = [t for t in threads if question.lower() in t['title'].lower()]
    return matches

@mcp.tool()
def post_ed_question(course_id: int, title: str, content: str, category: str = "General") -> dict:
    """
    Post a new question to Ed Discussion.
    """
    if not ed.api.api_token:
        return {"error": "Please provide your Ed Discussion API token to continue."}
    content_xml = f'<document version="2.0"><paragraph>{content}</paragraph></document>'
    result = ed.post_thread(course_id, title, content_xml, category)
    return {"result": result}

@mcp.tool()
def get_user_info() -> dict:
    """Get info about the currently authenticated Ed Discussion user."""
    if not ed.api.api_token:
        return {"error": "Please provide your Ed Discussion API token to continue."}
    return ed.get_user_info()

@mcp.tool()
def get_thread(thread_id: int) -> dict:
    """Get details for a specific Ed Discussion thread by thread ID."""
    if not ed.api.api_token:
        return {"error": "Please provide your Ed Discussion API token to continue."}
    return ed.get_thread(thread_id)

@mcp.tool()
def list_user_activity(user_id: int, course_id: int, limit: int = 10, filter: str = "all") -> list:
    """List a user's activity (threads/comments) in a course."""
    if not ed.api.api_token:
        return ["Please provide your Ed Discussion API token to continue."]
    return ed.list_user_activity(user_id, course_id, limit=limit, filter=filter)

@mcp.tool()
def upload_file(filename: str, content_type: str) -> dict:
    """Upload a file to Ed Discussion. Provide the local filename and its content type (e.g., 'image/png')."""
    if not ed.api.api_token:
        return {"error": "Please provide your Ed Discussion API token to continue."}
    return ed.upload_file(filename, content_type)

if __name__ == "__main__":
    mcp.run()