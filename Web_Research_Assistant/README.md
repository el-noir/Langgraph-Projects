# Web Research Assistant

🔬 **AI-powered research assistant with real-time streaming, beautiful UI, and comprehensive workflow visualization**

[![Next.js](https://img.shields.io/badge/Next.js-15.5-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-blue)](https://langchain-ai.github.io/langgraph/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)](https://www.typescriptlang.org/)

## ✨ Features

- 🎯 **Real-Time Streaming** - ChatGPT-style live report generation with typing effect
- 🔍 **Progressive Source Display** - Sources appear as they're discovered
- 📊 **5-Stage Workflow** - Search → Load → Summarize → Write → Finalize
- 🎨 **Beautiful Black & White UI** - Modern, minimalist design
- 📝 **Markdown Rendering** - Properly formatted reports with headings, lists, and citations
- 🔄 **Live Progress Tracking** - Real-time updates at each workflow stage
Web_Research_Assistant/
├── main.py                      # FastAPI backend with streaming endpoints
├── src/
│   └── worflow/
│       └── research_workflow.py # LangGraph workflow with streaming
├── client/                      # Next.js frontend application
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx         # Main UI with streaming
│   │       ├── layout.tsx       # Root layout
│   │       └── globals.css      # Styles & animations
│   ├── package.json             # Node dependencies
│   └── SETUP.md                 # Frontend setup guide
├── requirements_api.txt         # Python dependencies
├── .env                         # Environment variables
├── QUICKSTART.md                # Quick start guide
├── STREAMING.md                 # Streaming documentation
├── WORKFLOW_DIAGRAM.md          # Visual workflow diagrams
└── README.md                    # This file

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- API Keys: Google Gemini & Tavily

### 1. Setup Environment

Create `.env` file in root:
```env
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_search_api_key
```

### 2. Install Backend Dependencies

```bash
pip install -r requirements_api.txt
```

### 3. Install Frontend Dependencies

```bash
cd client
npm install
cd ..
```

### 4. Start Backend (Terminal 1)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Start Frontend (Terminal 2)

```bash
cd client
npm run dev
```

### 6. Access the Application

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

📖 **For detailed setup instructions, see [QUICKSTART.md](QUICKSTART.md)**

## 🔌 API Endpoints

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/research` | Non-streaming research (legacy) |
| `POST` | `/research/stream` | **Streaming research with real-time updates** |
| `GET` | `/docs` | Interactive API documentation (Swagger) |
| `GET` | `/redoc` | Alternative API documentation |

### Streaming Endpoint

The `/research/stream` endpoint uses Server-Sent Events (SSE) to stream:
- 🔍 Sources as they're discovered
- 📝 Report chunks as they're generated (typing effect)
- 📊 Progress updates at each workflow stage
- ✅ Final results with citations

**Event Types:**
- `status` - Workflow step updates
- `source_found` - Individual source discovered
- `report_chunk` - Report text chunk (50 chars)
- `result` - Final research results
- `error` - Error information

## 📝 Usage Examples

### Frontend (Recommended)

Simply visit http://localhost:3000 and enter your research query. The UI will:
1. Show sources as they're discovered
2. Display the report as it's being generated (typing effect)
3. Update progress in real-time
4. Show final results with citations

### Streaming API (Python)

```python
import requests

url = 'http://localhost:8000/research/stream'
params = {'query': 'Latest AI developments 2024'}

with requests.post(url, params=params, stream=True) as response:
    for line in response.iter_lines():
        if line.startswith(b'data: '):
            data = json.loads(line[6:])
            
            if data['type'] == 'source_found':
                print(f"Found: {data['source']['title']}")
            elif data['type'] == 'report_chunk':
                print(data['chunk'], end='', flush=True)
            elif data['type'] == 'result':
                print("\nResearch complete!")
```

### Non-Streaming API (Python)

```python
import requests

response = requests.post(
    'http://localhost:8000/research',
    params={'query': 'Latest AI developments 2024'}
)

result = response.json()
if result['success']:
    print(f"Report: {result['data']['report']}")
    print(f"Citations: {len(result['data']['citations'])}")
```

### cURL (Streaming)

```bash
curl -N -X POST "http://localhost:8000/research/stream?query=AI%20trends%202025"
```

## 📊 Streaming Events

### Status Event
```json
{
  "type": "status",
  "step": "searching",
  "message": "🔍 Found 10 sources",
  "progress": 20,
  "data": {"sources_found": 10}
}
```

### Source Found Event
```json
{
  "type": "source_found",
  "source": {
    "id": 1,
    "title": "AI Advances in 2024",
    "url": "https://example.com/ai-2024",
    "score": 0.95
  },
  "progress": 15
}
```

### Report Chunk Event
```json
{
  "type": "report_chunk",
  "chunk": "## AI Developments 2024\n\n**Executive Summary**\n",
  "progress": 85
}
```

### Result Event
```json
{
  "type": "result",
  "data": {
    "query": "Latest AI developments 2024",
    "sources_found": 10,
    "pages_processed": 10,
    "summaries_generated": 10,
    "report": "Full report text...",
    "citations": [{...}],
    "report_length": 7531,
    "timestamp": "2025-10-09 06:00:00"
  }
}
```

## 🎨 UI Features

### ChatGPT-Style Streaming
- **Live typing effect** - Report appears character by character
- **Blinking cursor** - Shows active generation
- **Progressive sources** - Sources appear as discovered
- **Clean design** - Minimal, focused interface
- **Real-time progress** - Smooth progress bar

### Markdown Rendering
- **Headings** (# and ##) - Large, bold section titles
- **Bold text** (\*\*text\*\*) - Emphasized content
- **Bullet lists** (* item) - Proper list formatting
- **Citations** ([1], [2]) - Blue superscript numbers
- **Proper spacing** - Comfortable reading experience

### Black & White Theme
- Professional minimalist design
- High contrast for readability
- Custom scrollbar styling
- Smooth animations

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Gemini API key | ✅ Yes |
| `TAVILY_API_KEY` | Tavily Search API key | ✅ Yes |

### Workflow Customization

Edit `src/worflow/research_workflow.py`:

- **Search limit**: `max_results=10` in `TavilySearch`
- **Chunk size**: `chunk_size=50` for streaming
- **Model**: `model="gemini-2.0-flash"`
- **Temperature**: `temperature=0.1`
- **Content limit**: `4000` characters per page

### Frontend Customization

Edit `client/src/app/globals.css`:

- **Colors**: Change `--background` and `--foreground`
- **Fonts**: Modify `--font-geist-sans`
- **Animations**: Adjust `fadeIn` duration

## 🧪 Testing

### Frontend Testing

1. Start both backend and frontend
2. Visit http://localhost:3000
3. Enter a test query: "Best restaurants in Riyadh"
4. Watch the streaming in action:
   - Sources appear progressively
   - Report types out like ChatGPT
   - Progress bar fills smoothly
   - Final results display with citations

### Backend Testing

**Test streaming endpoint:**
```bash
curl -N -X POST "http://localhost:8000/research/stream?query=AI%20trends"
```

**Test non-streaming endpoint:**
```bash
curl -X POST "http://localhost:8000/research?query=AI%20trends"
```

**View API docs:**
```
http://localhost:8000/docs
```

## 🚀 Deployment

### Frontend (Vercel)

```bash
cd client
vercel deploy
```

### Backend (Railway/Render)

1. Connect your GitHub repository
2. Set environment variables:
   - `GOOGLE_API_KEY`
   - `TAVILY_API_KEY`
3. Deploy from `main` branch

### Environment Variables in Production

**Backend:**
- `GOOGLE_API_KEY`
- `TAVILY_API_KEY`
- Update CORS origins in `main.py`

**Frontend:**
- Update API URL in `page.tsx` (line 45)
- Change from `http://localhost:8000` to your backend URL

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Complete setup guide
- **[STREAMING.md](STREAMING.md)** - Streaming implementation details
- **[WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md)** - Visual workflow diagrams
- **[client/SETUP.md](client/SETUP.md)** - Frontend setup guide

## 🎯 Workflow Stages

| Stage | Progress | Duration | Description |
|-------|----------|----------|-------------|
| **Initializing** | 0% | <1s | Starting workflow |
| **Searching** | 0-20% | 2-5s | Finding sources with Tavily |
| **Loading** | 20-40% | 5-15s | Extracting content from pages |
| **Summarizing** | 40-60% | 20-40s | AI summarization with Gemini |
| **Writing** | 60-95% | 10-20s | Report generation with Gemini |
| **Finalizing** | 95-100% | <1s | Processing citations |

**Total Time:** 40-80 seconds (varies by query complexity)

## 🎯 Performance Tips

- **Reduce sources**: Change `max_results=10` to `max_results=5`
- **Faster model**: Use `gemini-1.5-flash` instead of `gemini-2.0-flash`
- **Smaller chunks**: Reduce `chunk_size=50` to `chunk_size=25`
- **Skip content loading**: Comment out WebBaseLoader for faster results

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add pause/resume functionality
- [ ] Implement cancel button
- [ ] Save research history
- [ ] Export reports as PDF
- [ ] Add more citation formats
- [ ] Support multiple languages
- [ ] Add voice input
- [ ] Implement user authentication

## 📄 License

MIT License - feel free to use this project for learning and development!

## 🙏 Acknowledgments

- **LangChain & LangGraph** - Workflow orchestration
- **Google Gemini** - AI summarization and report generation
- **Tavily** - Web search API
- **Next.js** - Frontend framework
- **FastAPI** - Backend framework
- **Tailwind CSS** - Styling

---

## 🎉 Ready to Research!

1. **Start Backend**: `uvicorn main:app --reload`
2. **Start Frontend**: `cd client && npm run dev`
3. **Visit**: http://localhost:3000
4. **Enter Query**: "Best restaurants in Tokyo"
5. **Watch Magic**: See sources stream in and report generate live!

**Questions?** Check [QUICKSTART.md](QUICKSTART.md) or [STREAMING.md](STREAMING.md)
