FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY test_ed_api.py .

# Run the MCP server with stdio transport
ENTRYPOINT ["python", "main.py"] 