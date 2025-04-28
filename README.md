# Ed Discussion MCP Server

This server implements the Model Context Protocol (MCP) to allow Claude Desktop (or any MCP client) to access Ed Discussion. Using this server, you can search for relevant posts, post new questions, view thread details, and more - all from the Claude chat interface.

## Features

- ✅ Search for similar questions in Ed Discussion
- ✅ Post new questions to any Ed Discussion course board
- ✅ View detailed thread information
- ✅ List user activity
- ✅ Upload files to Ed Discussion
- ✅ Seamless authentication through Claude's chat interface

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the MCP server:**
   ```bash
   python main.py
   ```
   
   Or use the MCP CLI for development:
   ```bash
   mcp dev main.py
   ```

## Connecting to Claude Desktop

1. **Edit Claude Desktop configuration:**
   Open the Claude Desktop config file:
   
   - **Mac/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add your MCP server:**
   ```json
   {
      "mcpServers": {
         "ed-discussion": {
            "command": "/PATH/TO/python",
            "args": ["/PATH/TO/main.py"],
            "env": {
            "ED_API_TOKEN": "your-token-here"
            }
         }
      }
   }

   ```

3. **Restart Claude Desktop**

4. **First-time use:**
   - Add ED_API_TOKEN into your .env file with "ED_API_TOKEN=your-token-here" 

## Available MCP Tools

This server exposes the following tools to Claude:

| Tool | Description |
|------|-------------|
| `fetch_ed_posts` | Search for similar posts in a course |
| `post_ed_question` | Post a new question to a course |
| `get_user_info` | Get information about your user account |
| `get_thread` | Get detailed information about a specific thread |
| `list_user_activity` | See a user's recent activity in a course |
| `upload_file` | Upload a file to Ed Discussion |

## Finding Your Ed Discussion API Token

1. Log in to your Ed Discussion account
2. Go to Account Settings
3. Generate or copy your existing API token

## Example Usage in Claude

Once connected, you can ask Claude to:

- "Search for posts about final projects in course 12345"
- "Post a new question to course 12345 about homework submission"
- "Show me thread 67890 details"
- "What's my user info?"
- "Show my recent activity in course 12345"
- "Upload this file to Ed Discussion"

## References
- [edapi PyPI](https://pypi.org/project/edapi/)
- [edapi API Docs](https://github.com/smartspot2/edapi/blob/master/docs/api_docs.md)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) 