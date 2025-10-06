from fastapi import FastAPI

app = FastAPI(title="API Gateway for Distributed LLM Serving System")
# Health check endpoint-- occasionally check if the service is up
@app.get("/healthz", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}

