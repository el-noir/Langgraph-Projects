# Web Research Assistant - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
1. **Python 3.9+** with pip installed
2. **Node.js 18+** with npm installed
3. **API Keys** (required):
   - `GOOGLE_API_KEY` - For Google Gemini AI
   - `TAVILY_API_KEY` - For web search

### Step 1: Setup Environment Variables

Create a `.env` file in the root directory:

```bash
# .env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Step 2: Install Backend Dependencies

```bash
# Install Python dependencies
pip install -r requirements_api.txt
```

### Step 3: Install Frontend Dependencies

```bash
# Navigate to client directory
cd client

# Install Node dependencies
npm install

# Return to root
cd ..
```

### Step 4: Run the Application

#### Option A: Run Both Services (Recommended)

**Terminal 1 - Backend:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
```

#### Option B: Test Backend Only
```bash
python src/worflow/research_workflow.py
```

### Step 5: Access the Application

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📝 Usage

1. Open http://localhost:3000 in your browser
2. Enter a research query (e.g., "Latest developments in AI 2025")
3. Click "Start Research"
4. Wait for the AI to:
   - Search multiple web sources
   - Extract and analyze content
   - Generate summaries
   - Create a comprehensive report
5. View the results with citations

## 🎨 Features

### Black & White Theme
- Clean, minimalist design
- Professional appearance
- Easy to read reports
- Responsive layout

### Research Capabilities
- **Multi-source search** - Searches 10+ web sources
- **Content extraction** - Extracts full page content
- **AI summarization** - Summarizes each source
- **Report generation** - Creates comprehensive reports
- **Citation tracking** - Properly cites all sources

## 🔧 API Testing

### Using curl:
```bash
curl -X POST "http://localhost:8000/research?query=artificial%20intelligence%202025"
```

### Using Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/research",
    params={"query": "artificial intelligence 2025"}
)
print(response.json())
```

## 📊 Expected Output

The API returns:
```json
{
  "success": true,
  "data": {
    "query": "artificial intelligence 2025",
    "sources_found": 10,
    "pages_processed": 10,
    "summaries_generated": 10,
    "report": "# Executive Summary\n\n...",
    "citations": [
      {
        "id": 1,
        "title": "...",
        "url": "...",
        "access_date": "2025-10-09",
        "relevance_score": 0.95
      }
    ],
    "report_length": 5000,
    "timestamp": "2025-10-09 05:40:00"
  }
}
```

## 🐛 Troubleshooting

### Backend Issues

**Error: "Could not import module 'app'"**
- Solution: Use `uvicorn main:app` not `uvicorn app:main`

**Error: "API key not found"**
- Solution: Make sure `.env` file exists with valid API keys

**Error: "Module not found"**
- Solution: Install dependencies with `pip install -r requirements_api.txt`

### Frontend Issues

**Error: "Connection refused"**
- Solution: Make sure backend is running on port 8000

**Error: "CORS error"**
- Solution: Already configured in `main.py`, restart backend

**Error: "Module not found"**
- Solution: Run `npm install` in the `client/` directory

## 📁 Project Structure

```
Web_Research_Assistant/
├── main.py                    # FastAPI backend entry point
├── requirements_api.txt       # Python dependencies
├── .env                       # Environment variables (create this)
├── src/
│   └── worflow/
│       └── research_workflow.py  # LangGraph workflow
└── client/                    # Next.js frontend
    ├── src/
    │   └── app/
    │       ├── page.tsx       # Main UI
    │       ├── layout.tsx     # Layout
    │       └── globals.css    # Styles
    └── package.json           # Node dependencies
```

## 🎯 Next Steps

1. **Customize the theme** - Edit `client/src/app/globals.css`
2. **Add more features** - Extend the workflow in `research_workflow.py`
3. **Deploy** - Use Vercel for frontend, Railway/Render for backend
4. **Add authentication** - Implement user accounts
5. **Save research history** - Add database integration

## 📚 Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 🤝 Support

If you encounter issues:
1. Check that all dependencies are installed
2. Verify API keys are correct
3. Ensure both services are running
4. Check console logs for errors
