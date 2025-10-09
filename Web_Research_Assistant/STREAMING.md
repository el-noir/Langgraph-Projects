# Streaming Functionality Documentation

## Overview
The Web Research Assistant now features **real-time streaming** of workflow progress, similar to chatbot streaming. This provides live updates as the research progresses through each stage.

## Features

### 🔄 Real-Time Workflow Visualization
- **Live Progress Bar** - Shows completion percentage (0-100%)
- **Step-by-Step Updates** - Each workflow stage is displayed as it executes
- **Detailed Metrics** - Real-time data for each step (sources found, pages processed, etc.)
- **Timestamps** - Each step shows when it was completed
- **Visual Indicators** - Icons show status (in-progress, completed, failed)

### 📊 Workflow Stages Tracked

1. **Initializing** (0%) - Starting the research workflow
2. **Searching** (20%) - Web search using Tavily
   - Shows: Number of sources found
3. **Loading** (40%) - Content extraction from web pages
   - Shows: Number of pages processed
4. **Summarizing** (60%) - AI summarization of each page
   - Shows: Number of summaries generated
5. **Writing** (80%) - Comprehensive report generation
   - Shows: Report length in characters
6. **Finalizing** (95%) - Citation processing and caching
   - Shows: Number of citations
7. **Completed** (100%) - Research finished successfully

## Technical Implementation

### Backend (FastAPI + LangGraph)

#### 1. Streaming Endpoint
**File:** `main.py`

```python
@app.post("/research/stream")
async def research_stream(query: str):
    """Streaming research endpoint with real-time progress updates"""
    
    async def event_generator():
        for update in run_research_stream(query):
            event_data = json.dumps(update)
            yield f"data: {event_data}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

#### 2. Streaming Workflow Function
**File:** `src/worflow/research_workflow.py`

```python
def run_research_stream(query: str, thread_id: str = None):
    """
    Run end-to-end research workflow with streaming progress updates
    
    Yields:
        Dict containing progress updates and final results
    """
    # Stream through the workflow
    for event in research_workflow.stream(initial_state, config):
        if "web_search" in event:
            yield {
                "type": "status",
                "step": "searching",
                "message": "🔍 Searching web sources...",
                "progress": 20,
                "data": {"sources_found": len(state.get("search_results", []))}
            }
        # ... other steps
```

### Frontend (Next.js + React)

#### 1. Server-Sent Events (SSE) Handler
**File:** `client/src/app/page.tsx`

```typescript
const response = await fetch(`http://localhost:8000/research/stream?query=${encodeURIComponent(query)}`, {
  method: 'POST',
});

const reader = response.body?.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      
      if (data.type === 'status') {
        // Update workflow steps
        setWorkflowSteps(prev => [...prev, data]);
        setCurrentProgress(data.progress);
      } else if (data.type === 'result') {
        // Final result received
        setResult(data.data);
      }
    }
  }
}
```

#### 2. Workflow Step Display

```tsx
{workflowSteps.map((step, index) => (
  <div key={index} className="flex items-start gap-4">
    <div className="w-6 h-6 border-2 border-black rounded-full">
      <div className="w-2 h-2 bg-black rounded-full animate-pulse"></div>
    </div>
    <div>
      <p className="font-medium">{step.message}</p>
      {step.data && (
        <div className="text-sm text-gray-600">
          {step.data.sources_found && <p>• Found {step.data.sources_found} sources</p>}
        </div>
      )}
    </div>
  </div>
))}
```

## Event Types

### Status Event
```json
{
  "type": "status",
  "step": "searching",
  "message": "🔍 Searching web sources...",
  "progress": 20,
  "data": {
    "sources_found": 10
  }
}
```

### Result Event
```json
{
  "type": "result",
  "data": {
    "query": "...",
    "sources_found": 10,
    "pages_processed": 10,
    "summaries_generated": 10,
    "report": "...",
    "citations": [...],
    "report_length": 5000,
    "timestamp": "2025-10-09 05:50:00"
  }
}
```

### Error Event
```json
{
  "type": "error",
  "step": "failed",
  "message": "❌ Workflow failed: ...",
  "error": "Error details"
}
```

## UI Components

### Progress Bar
- **Width:** Full container width
- **Height:** 2px (h-2)
- **Color:** Black on gray background
- **Animation:** Smooth transition (duration-500)
- **Display:** Shows percentage (0-100%)

### Workflow Steps
- **Layout:** Vertical timeline
- **Icons:** 
  - In-progress: Pulsing dot
  - Completed: Checkmark in black circle
  - Failed: X in red circle
- **Data:** Shows relevant metrics for each step
- **Timestamp:** Local time when step completed
- **Animation:** Fade-in effect (0.3s)

## Usage

### Start a Streaming Research

```bash
# Backend must be running
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Frontend must be running
cd client
npm run dev
```

### Test the Endpoint Directly

```bash
# Using curl
curl -N -X POST "http://localhost:8000/research/stream?query=artificial%20intelligence"

# Output will stream like:
# data: {"type":"status","step":"initializing","message":"🔬 Starting...","progress":0}
# data: {"type":"status","step":"searching","message":"🔍 Searching...","progress":20}
# ...
```

## Benefits

1. **Better UX** - Users see progress instead of waiting blindly
2. **Transparency** - Clear visibility into what the AI is doing
3. **Debugging** - Easier to identify where issues occur
4. **Engagement** - Users stay engaged during long operations
5. **Trust** - Builds confidence by showing the research process

## Comparison: Streaming vs Non-Streaming

| Feature | Non-Streaming | Streaming |
|---------|--------------|-----------|
| User Feedback | None until complete | Real-time updates |
| Progress Visibility | Hidden | Visible (0-100%) |
| Step Details | Not shown | Detailed metrics |
| Error Detection | At the end | Immediate |
| User Experience | Waiting blindly | Engaged watching |
| Debugging | Difficult | Easy |

## Browser Compatibility

- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ⚠️ IE11 (Not supported - use polyfill)

## Performance Considerations

- **Network:** SSE maintains an open connection
- **Memory:** Workflow steps accumulate in state
- **CPU:** Minimal - just JSON parsing
- **Bandwidth:** ~1-2KB per update, ~10-20KB total

## Future Enhancements

1. **Pause/Resume** - Allow users to pause research
2. **Cancel** - Abort ongoing research
3. **History** - Save and replay workflow steps
4. **Export** - Download workflow timeline
5. **Notifications** - Browser notifications on completion
6. **WebSocket** - Bi-directional communication
7. **Progress Estimates** - Time remaining predictions

## Troubleshooting

### No Updates Appearing
- Check browser console for errors
- Verify backend is using `/research/stream` endpoint
- Ensure CORS is configured correctly

### Updates Stop Mid-Stream
- Check backend logs for errors
- Verify API keys are valid
- Check network connection

### Slow Updates
- Normal - some steps (summarization, report writing) take longer
- LLM API calls can be slow
- Network latency affects update speed

## Related Files

- `main.py` - Streaming endpoint
- `src/worflow/research_workflow.py` - Streaming workflow function
- `client/src/app/page.tsx` - Frontend SSE handler
- `client/src/app/globals.css` - Animations

## API Reference

### POST /research/stream

**Parameters:**
- `query` (string, required) - Research query

**Response:**
- Content-Type: `text/event-stream`
- Format: Server-Sent Events (SSE)
- Events: status, result, error

**Example:**
```bash
POST http://localhost:8000/research/stream?query=AI%20trends%202025
```

## Conclusion

The streaming functionality transforms the research experience from a black-box operation into a transparent, engaging process. Users can now watch as the AI searches, analyzes, and synthesizes information in real-time, building trust and improving the overall user experience.
