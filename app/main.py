from fastapi import FastAPI, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.application.orchestrator import Orchestrator

app = FastAPI(title="Cindy - Voice Chat Assistant")

# Dependency Injection (Singleton for simplicity here)
orchestrator = Orchestrator()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint.
    Recieves text, returns text + audio + metadata.
    """
    try:
        response = orchestrator.process_request(request)
        return response
    except Exception as e:
        # In a real app, you'd log this properly
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}
