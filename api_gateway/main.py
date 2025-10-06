from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from fastapi.responses import RedirectResponse


app = FastAPI(title="API Gateway for Distributed LLM Serving System")
# Health check endpoint-- occasionally check if the service is up
@app.get("/healthz", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt")
    stream: bool = False  # 先占位，暂不实现流式

@app.post("/chat", tags=["Chat"])
def chat(request: ChatRequest):
    reply_text = f"Echo: {request.prompt}"
    # Simulate a response structure similar to OpenAI's ChatCompletion
    return {
        "id": f"chatcmpl-local-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(datetime.utcnow().timestamp()),
        "model": "echo-mvp",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": reply_text},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": len(request.prompt.split()),
            "completion_tokens": len(reply_text.split()),
            "total_tokens": len(request.prompt.split()) + len(reply_text.split()),
        },
    }


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs")
# Redirect root to docs


    




