FROM python:3.12-slim

WORKDIR /app
COPY api_gateway/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0]
