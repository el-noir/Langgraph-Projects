from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from src.worflow.research_workflow import run_research, run_research_stream, format_research_response
import json

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/research")
def research(query: str):
    """Non-streaming research endpoint (legacy)"""
    result = run_research(query)
    formatted_response = format_research_response(result)
    return formatted_response


@app.post("/research/stream")
async def research_stream(query: str):
    """Streaming research endpoint with real-time progress updates"""
    
    async def event_generator():
        try:
            for update in run_research_stream(query):
                # Format as Server-Sent Events (SSE)
                event_data = json.dumps(update)
                yield f"data: {event_data}\n\n"
        except Exception as e:
            error_data = json.dumps({
                "type": "error",
                "message": f"Stream error: {str(e)}",
                "error": str(e)
            })
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

