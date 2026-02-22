FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir fastmcp uvicorn mlflow pandas requests

COPY mcp_server.py .

CMD ["python", "mcp_server.py"]