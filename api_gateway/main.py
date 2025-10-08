from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from fastapi.responses import RedirectResponse
import httpx
import uuid
from prometheus_client import Counter, Histogram,generate_latest,CONTENT_TYPE_LATEST


app = FastAPI(title="API Gateway for Distributed LLM Serving System")
# Health check endpoint-- occasionally check if the service is up
@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt")
    stream: bool = False  # 先占位，暂不实现流式

# the vllm is listening to the 8000 port
VLLM_BASE = "https://transgressively-wantless-lakiesha.ngrok-free.dev"
MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

@app.post("/chat", tags=["Chat"])
async def chat(request: ChatRequest):
    start = time.time()
    try:
        reply_text = f"Echo: {request.prompt}"
        # Simulate a response structure similar to OpenAI's ChatCompletion
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": request.prompt},
                {"role": "assistant", "content": reply_text}
            ],
            "stream": False,
        }
        async with httpx.AsyncClient() as client:
            # 本来是服务端暴露接口，但是同时也是客户端，去请求vllm服务
            response = await client.post(f"{VLLM_BASE}/v1/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
        REQS.labels( endpoint="/chat").inc()
        return data
    except Exception as e:
        ERRS.labels("/chat", type(e).__name__).inc()
        REQS.labels("/chat","500").inc()
        return {"error": str(e)}
    finally:
        LAT.labels( endpoint="/chat").observe(time.time() - start)






@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs")
# Redirect root to docs

REQS = Counter('api_requests_total', 'Total API Requests', ['endpoint','status'])
ERRS = Counter('api_errors_total', 'Total API Errors', ['endpoint','error_type'])
LAT = Histogram('api_request_latency_seconds', 'API Request Latency', ['endpoint'])

@app.get("/metrics", include_in_schema=False)
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)




    




