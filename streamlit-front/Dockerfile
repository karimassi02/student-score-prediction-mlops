FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir streamlit mcp requests

COPY app.py .

ENV PORT=8080

CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0