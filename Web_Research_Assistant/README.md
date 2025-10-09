# Web Research Assistant API

🔬 **AI-powered research assistant using LangGraph workflow served via FastAPI**

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   LangGraph      │    │   External      │
│   main.py       │───▶│   Workflow       │───▶│   Services      │
│                 │    │   research_      │    │                 │
│   • /research   │    │   workflow.py    │    │   • Tavily      │
│   • /health     │    │                  │    │   • Google AI   │
│   • /sessions   │    │   Nodes:         │    │   • Web Pages   │
└─────────────────┘    │   • web_search   │    └─────────────────┘
                       │   • content_     │
                       │     loader       │
                       │   • summarizer   │
                       │   • report_      │
                       │     writer       │
                       │   • citation_    │
                       │     cache        │
                       └──────────────────┘
```

## 📁 Project Structure

```
Web_Research_Assistant/
├── main.py                 # FastAPI application with research routes
├── research_workflow.py    # LangGraph workflow implementation
├── start_api.py           # API startup script
├── test_api.py            # API testing suite
├── requirements_api.txt   # Python dependencies
├── .env                   # Environment variables
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_api.txt
```

Or install core packages:
```bash
pip install fastapi uvicorn langchain langgraph langchain-google-genai langchain-tavily langchain-community
```

### 2. Set Environment Variables

Create a `.env` file:
```env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Start the API

Option A - Using startup script:
```bash
python start_api.py
```

Option B - Direct uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the API

```bash
python test_api.py
```

## 🔌 API Endpoints

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and available endpoints |
| `GET` | `/health` | Health check |
| `POST` | `/research` | Conduct comprehensive research |
| `GET` | `/research/samples` | Get sample queries and usage examples |

### Session Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/research/sessions` | List all research sessions |
| `GET` | `/research/session/{thread_id}` | Get specific research session |
| `DELETE` | `/research/sessions` | Clear all sessions |

### Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/docs` | Interactive API documentation (Swagger) |
| `GET` | `/redoc` | Alternative API documentation |

## 📝 Usage Examples

### Python Request

```python
import requests

# Conduct research
response = requests.post(
    'http://localhost:8000/research',
    json={
        'query': 'Latest developments in artificial intelligence 2024',
        'thread_id': 'my_research_session'  # Optional
    }
)

result = response.json()
if result['success']:
    print(f"Report: {result['data']['report']}")
    print(f"Citations: {len(result['data']['citations'])}")
else:
    print(f"Error: {result['error']}")
```

### cURL Request

```bash
curl -X POST "http://localhost:8000/research" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Latest developments in artificial intelligence 2024"
     }'
```

### JavaScript/Fetch

```javascript
fetch('http://localhost:8000/research', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        query: 'Latest developments in artificial intelligence 2024'
    })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Report:', data.data.report);
    } else {
        console.error('Error:', data.error);
    }
});
```

## 📊 Response Format

### Research Endpoint Response

```json
{
  "success": true,
  "error": null,
  "data": {
    "query": "Latest developments in artificial intelligence 2024",
    "sources_found": 5,
    "pages_processed": 5,
    "summaries_generated": 5,
    "report": "## AI Developments 2024\n\n**Executive Summary**\n...",
    "citations": [
      {
        "id": 1,
        "title": "AI Advances in 2024",
        "url": "https://example.com/ai-2024",
        "access_date": "2024-10-09",
        "citation_format": "[1] AI Advances in 2024. Retrieved 2024-10-09. https://example.com/ai-2024"
      }
    ],
    "report_length": 7531,
    "timestamp": "2024-10-09 15:30:45"
  },
  "processing_time": 45.67
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Gemini API key for LLM operations | ✅ Yes |
| `TAVILY_API_KEY` | Tavily API key for web search | ✅ Yes |

### Workflow Parameters

Edit `research_workflow.py` to customize:

- **Search results limit**: Modify `max_results` in `TavilySearch`
- **Content length**: Adjust content truncation in `content_loader`
- **Model settings**: Change temperature, model version in `ChatGoogleGenerativeAI`
- **Prompt templates**: Customize system prompts for different node behaviors

## 🧪 Testing

### Run Test Suite

```bash
python test_api.py
```

Tests include:
- ✅ Health check
- ✅ Sample queries endpoint
- ✅ Full research workflow
- ✅ Session management

### Manual Testing

1. **Health Check**: `GET http://localhost:8000/health`
2. **Sample Queries**: `GET http://localhost:8000/research/samples`
3. **Research**: `POST http://localhost:8000/research` with JSON body
4. **Documentation**: Visit `http://localhost:8000/docs`

## 🚀 Production Deployment

### 1. Security Considerations

- Set specific CORS origins instead of `["*"]`
- Add authentication/API key validation
- Use environment-specific configurations
- Implement rate limiting

### 2. Database Integration

Replace in-memory session storage:

```python
# Instead of: research_sessions: Dict[str, Dict[str, Any]] = {}
# Use: Database connection (PostgreSQL, MongoDB, etc.)
```

### 3. Scaling Options

- **Horizontal**: Deploy multiple API instances behind load balancer
- **Async**: Implement background task processing for long research queries
- **Caching**: Add Redis for caching research results
- **Queue**: Use Celery/RQ for workflow task queuing

### 4. Monitoring

- Add logging with structured format
- Implement health checks for external services
- Monitor API response times and error rates
- Track research workflow success/failure rates

## 🔗 Related Files

- **Notebook**: `workflow.ipynb` - Interactive development environment
- **Original workflow**: Developed and tested in Jupyter notebook
- **Migration**: Workflow extracted to `research_workflow.py` for API use

## 🆘 Troubleshooting

### Common Issues

1. **Import errors**: Install missing packages with `pip install -r requirements_api.txt`
2. **API key errors**: Check `.env` file and environment variable names
3. **Port conflicts**: Change port in `start_api.py` or `uvicorn` command
4. **SSL errors**: WebBaseLoader handles SSL gracefully with fallbacks

### Debug Mode

Start with verbose logging:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### Performance Issues

- Reduce `max_results` in search configuration
- Implement caching for repeated queries
- Use async processing for long-running research

---

🎉 **Ready to conduct AI-powered research!** Visit `http://localhost:8000/docs` for interactive API documentation.