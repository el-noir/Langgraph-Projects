from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.worflow.research_workflow import run_research, format_research_response

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
    result = run_research(query)
    formatted_response = format_research_response(result)
    return formatted_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

