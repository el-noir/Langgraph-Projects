"""
Web Research Assistant API
=========================

FastAPI application providing research endpoints using LangGraph workflow.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uvicorn
import asyncio
import time
from datetime import datetime

# Import our research workflow
from research_workflow import run_research, format_research_response

# Initialize FastAPI app
app = FastAPI(
    title="Web Research Assistant API",
    description="AI-powered web research assistant using LangGraph workflow",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ResearchRequest(BaseModel):
    query: str = Field(..., description="Research question or topic", min_length=5, max_length=500)
    thread_id: Optional[str] = Field(None, description="Optional session thread ID")

class ResearchResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# In-memory storage for research sessions (in production, use a database)
research_sessions: Dict[str, Dict[str, Any]] = {}

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "Web Research Assistant API",
        "version": "1.0.0",
        "description": "AI-powered research assistant using LangGraph",
        "endpoints": {
            "research": "/research - POST - Conduct research on a topic",
            "health": "/health - GET - Check API health",
            "docs": "/docs - GET - API documentation"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    """
    Conduct comprehensive web research on a given topic
    
    This endpoint runs the complete LangGraph workflow including:
    - Web search using Tavily
    - Content extraction from web pages
    - Document summarization
    - Report generation
    - Citation management
    """
    start_time = time.time()
    
    try:
        # Validate input
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Generate thread ID if not provided
        thread_id = request.thread_id or f"research_{int(time.time())}"
        
        print(f"🔬 API: Starting research for query: '{request.query}'")
        print(f"📝 Thread ID: {thread_id}")
        
        # Run the research workflow
        result = run_research(request.query, thread_id)
        
        # Format the response
        formatted_result = format_research_response(result)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Store session (optional - for session management)
        research_sessions[thread_id] = {
            "query": request.query,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "processing_time": processing_time
        }
        
        # Add processing time to response
        response = ResearchResponse(
            success=formatted_result["success"],
            error=formatted_result["error"],
            data=formatted_result["data"],
            processing_time=round(processing_time, 2)
        )
        
        print(f"✅ API: Research completed in {processing_time:.2f} seconds")
        
        return response
        
    except Exception as e:
        processing_time = time.time() - start_time
        error_msg = f"Research failed: {str(e)}"
        print(f"❌ API: {error_msg}")
        
        return ResearchResponse(
            success=False,
            error=error_msg,
            data=None,
            processing_time=round(processing_time, 2)
        )

@app.get("/research/session/{thread_id}")
async def get_research_session(thread_id: str):
    """
    Retrieve a previous research session by thread ID
    """
    if thread_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Research session not found")
    
    session = research_sessions[thread_id]
    formatted_result = format_research_response(session["result"])
    
    return {
        "thread_id": thread_id,
        "query": session["query"],
        "timestamp": session["timestamp"],
        "processing_time": session["processing_time"],
        "result": formatted_result
    }

@app.get("/research/sessions")
async def list_research_sessions():
    """
    List all research sessions
    """
    sessions = []
    for thread_id, session in research_sessions.items():
        sessions.append({
            "thread_id": thread_id,
            "query": session["query"],
            "timestamp": session["timestamp"],
            "processing_time": session["processing_time"],
            "success": session["result"].get("error_message") is None
        })
    
    return {
        "total_sessions": len(sessions),
        "sessions": sorted(sessions, key=lambda x: x["timestamp"], reverse=True)
    }

@app.delete("/research/sessions")
async def clear_research_sessions():
    """
    Clear all research sessions
    """
    count = len(research_sessions)
    research_sessions.clear()
    return {"message": f"Cleared {count} research sessions"}

# Sample queries endpoint for testing
@app.get("/research/samples")
async def get_sample_queries():
    """
    Get sample research queries for testing
    """
    return {
        "sample_queries": [
            "Latest developments in artificial intelligence 2024",
            "Climate change impacts on global agriculture",
            "Quantum computing breakthroughs and applications",
            "Sustainable transportation innovations",
            "Cybersecurity trends and threats 2024",
            "Renewable energy technologies advancement",
            "Space exploration missions and discoveries",
            "Medical breakthroughs in cancer treatment",
            "Future of remote work and digital nomadism",
            "Blockchain technology real-world applications"
        ],
        "usage_examples": {
            "curl": "curl -X POST 'http://localhost:8000/research' -H 'Content-Type: application/json' -d '{\"query\": \"Your research topic here\"}'",
            "python": """
import requests

response = requests.post(
    'http://localhost:8000/research',
    json={'query': 'Your research topic here'}
)
result = response.json()
print(result['data']['report'])
""",
            "javascript": """
fetch('http://localhost:8000/research', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query: 'Your research topic here'})
})
.then(response => response.json())
.then(data => console.log(data.data.report));
"""
        }
    }

if __name__ == "__main__":
    print("🚀 Starting Web Research Assistant API...")
    print("📊 LangGraph workflow integration enabled")
    print("🔍 Research endpoints available at http://localhost:8000")
    print("📖 API documentation at http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )