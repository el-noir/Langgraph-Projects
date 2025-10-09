# Web Research Assistant - Workflow Diagram

## Complete Streaming Workflow

```mermaid
graph TD
    A[User Enters Query] --> B[Frontend: POST /research/stream]
    B --> C[Backend: FastAPI Endpoint]
    C --> D[Initialize Workflow State]
    
    D --> E1[Step 1: Web Search 🔍]
    E1 --> E1a[Stream: Initializing 0%]
    E1a --> E1b[Tavily Search API]
    E1b --> E1c[Stream: Searching 20%]
    E1c --> E1d[Return: sources_found]
    
    E1d --> E2[Step 2: Content Loader 📄]
    E2 --> E2a[Stream: Loading 40%]
    E2a --> E2b[WebBaseLoader for each URL]
    E2b --> E2c[Extract & Clean Content]
    E2c --> E2d[Return: pages_processed]
    
    E2d --> E3[Step 3: Summarizer 📝]
    E3 --> E3a[Stream: Summarizing 60%]
    E3a --> E3b[Google Gemini API]
    E3b --> E3c[Summarize Each Page]
    E3c --> E3d[Return: summaries_generated]
    
    E3d --> E4[Step 4: Report Writer 📊]
    E4 --> E4a[Stream: Writing 80%]
    E4a --> E4b[Google Gemini API]
    E4b --> E4c[Generate Comprehensive Report]
    E4c --> E4d[Return: report_length]
    
    E4d --> E5[Step 5: Citation Cache 📚]
    E5 --> E5a[Stream: Finalizing 95%]
    E5a --> E5b[Format Citations]
    E5b --> E5c[Cache Results]
    E5c --> E5d[Return: citations_count]
    
    E5d --> F[Stream: Completed 100%]
    F --> G[Send Final Result]
    G --> H[Frontend: Display Results]
    
    H --> H1[Show Statistics]
    H --> H2[Display Report]
    H --> H3[List Citations]
    
    style E1 fill:#f0f0f0
    style E2 fill:#f0f0f0
    style E3 fill:#f0f0f0
    style E4 fill:#f0f0f0
    style E5 fill:#f0f0f0
    style F fill:#90EE90
    style A fill:#FFE4B5
    style H fill:#ADD8E6
```

## Frontend State Flow

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Streaming: User Submits Query
    
    Streaming --> Initializing: 0%
    Initializing --> Searching: 20%
    Searching --> Loading: 40%
    Loading --> Summarizing: 60%
    Summarizing --> Writing: 80%
    Writing --> Finalizing: 95%
    Finalizing --> Completed: 100%
    
    Completed --> DisplayResults
    DisplayResults --> Idle: New Query
    
    Streaming --> Error: Exception
    Error --> Idle: Retry
    
    note right of Streaming
        SSE Connection Open
        Receiving Updates
    end note
    
    note right of DisplayResults
        Show Report
        Show Citations
        Show Statistics
    end note
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant FastAPI
    participant LangGraph
    participant TavilyAPI
    participant GeminiAPI
    
    User->>Frontend: Enter Query
    Frontend->>FastAPI: POST /research/stream
    FastAPI->>LangGraph: run_research_stream()
    
    LangGraph->>Frontend: Stream: Initializing (0%)
    
    LangGraph->>TavilyAPI: Search Query
    TavilyAPI-->>LangGraph: Search Results
    LangGraph->>Frontend: Stream: Searching (20%)
    
    loop For Each URL
        LangGraph->>LangGraph: Load Content
    end
    LangGraph->>Frontend: Stream: Loading (40%)
    
    loop For Each Page
        LangGraph->>GeminiAPI: Summarize Content
        GeminiAPI-->>LangGraph: Summary
    end
    LangGraph->>Frontend: Stream: Summarizing (60%)
    
    LangGraph->>GeminiAPI: Generate Report
    GeminiAPI-->>LangGraph: Full Report
    LangGraph->>Frontend: Stream: Writing (80%)
    
    LangGraph->>LangGraph: Process Citations
    LangGraph->>Frontend: Stream: Finalizing (95%)
    
    LangGraph->>Frontend: Stream: Completed (100%)
    LangGraph->>Frontend: Final Result Data
    
    Frontend->>User: Display Results
```

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Search Form │  │  Progress Bar│  │ Workflow Steps│      │
│  │              │  │   0-100%     │  │   Timeline    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Results    │  │    Report    │  │   Citations   │      │
│  │  Statistics  │  │   Display    │  │     List      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│                    SSE Handler (EventSource)                 │
└─────────────────────────────────────────────────────────────┘
                              ↕
                    HTTP/SSE Connection
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Streaming Endpoint                       │  │
│  │         POST /research/stream                         │  │
│  │                                                        │  │
│  │  • Receives query                                     │  │
│  │  • Calls run_research_stream()                        │  │
│  │  • Yields SSE events                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↕                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              LangGraph Workflow                       │  │
│  │                                                        │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │  │
│  │  │ Web Search │→ │  Content   │→ │ Summarizer │     │  │
│  │  │   Agent    │  │   Loader   │  │            │     │  │
│  │  └────────────┘  └────────────┘  └────────────┘     │  │
│  │         ↓                ↓                ↓           │  │
│  │  ┌────────────┐  ┌────────────┐                      │  │
│  │  │   Report   │→ │ Citation   │                      │  │
│  │  │   Writer   │  │   Cache    │                      │  │
│  │  └────────────┘  └────────────┘                      │  │
│  │                                                        │  │
│  │  Each node yields progress updates                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                              ↕                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              External APIs                            │  │
│  │                                                        │  │
│  │  • Tavily Search API (Web Search)                     │  │
│  │  • Google Gemini API (Summarization & Report)         │  │
│  │  • WebBaseLoader (Content Extraction)                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Workflow Step Details

### Step 1: Web Search (20%)
```
Input:  User query
Action: Search web using Tavily API
Output: List of URLs with titles and snippets
Stream: {"step": "searching", "progress": 20, "data": {"sources_found": 10}}
```

### Step 2: Content Loader (40%)
```
Input:  List of URLs
Action: Extract full content from each URL
Output: Cleaned page content
Stream: {"step": "loading", "progress": 40, "data": {"pages_processed": 10}}
```

### Step 3: Summarizer (60%)
```
Input:  Page contents
Action: AI summarization of each page
Output: Individual summaries
Stream: {"step": "summarizing", "progress": 60, "data": {"summaries_generated": 10}}
```

### Step 4: Report Writer (80%)
```
Input:  All summaries
Action: Generate comprehensive report
Output: Full research report
Stream: {"step": "writing", "progress": 80, "data": {"report_length": 5000}}
```

### Step 5: Citation Cache (95%)
```
Input:  Summaries and report
Action: Format citations and cache
Output: Structured citations
Stream: {"step": "finalizing", "progress": 95, "data": {"citations_count": 10}}
```

### Step 6: Completed (100%)
```
Input:  All workflow results
Action: Format final response
Output: Complete research package
Stream: {"step": "completed", "progress": 100}
        {"type": "result", "data": {...}}
```

## UI State Transitions

```
┌──────────────┐
│  Empty State │  ← Initial load
└──────┬───────┘
       │ User enters query
       ↓
┌──────────────┐
│   Loading    │  ← Show progress bar & workflow steps
│   State      │
└──────┬───────┘
       │ Research completes
       ↓
┌──────────────┐
│   Results    │  ← Display report, citations, stats
│   State      │
└──────┬───────┘
       │ New query
       ↓
┌──────────────┐
│   Loading    │  ← Reset and start again
│   State      │
└──────────────┘
```

## Error Handling Flow

```mermaid
graph LR
    A[Streaming Active] --> B{Error Occurs?}
    B -->|No| C[Continue to Next Step]
    B -->|Yes| D[Catch Exception]
    D --> E[Stream Error Event]
    E --> F[Display Error Message]
    F --> G[Set Loading = False]
    G --> H[User Can Retry]
    
    style D fill:#ffcccc
    style E fill:#ffcccc
    style F fill:#ffcccc
```

## Performance Metrics

| Stage | Typical Duration | API Calls | Network |
|-------|-----------------|-----------|---------|
| Initializing | < 1s | 0 | Minimal |
| Searching | 2-5s | 1 (Tavily) | Medium |
| Loading | 5-15s | 10 (HTTP) | High |
| Summarizing | 20-40s | 10 (Gemini) | High |
| Writing | 10-20s | 1 (Gemini) | Medium |
| Finalizing | < 1s | 0 | Minimal |
| **Total** | **40-80s** | **22** | **High** |

## Key Technologies

- **Backend:** FastAPI, LangGraph, LangChain
- **Frontend:** Next.js 15, React 19, TypeScript
- **Streaming:** Server-Sent Events (SSE)
- **APIs:** Tavily Search, Google Gemini
- **Styling:** Tailwind CSS 4
- **State:** React useState hooks

## Benefits of Streaming Architecture

1. **Real-Time Feedback** - Users see progress immediately
2. **Better UX** - No black-box waiting
3. **Transparency** - Clear visibility into AI operations
4. **Debugging** - Easy to identify bottlenecks
5. **Engagement** - Users stay engaged during long operations
6. **Trust** - Builds confidence by showing the process
7. **Cancellation** - Potential to cancel mid-stream (future)

## Conclusion

The streaming architecture transforms the research experience from a synchronous, blocking operation into an engaging, transparent process. Users can watch as the AI searches, analyzes, and synthesizes information in real-time, creating a more interactive and trustworthy experience.
