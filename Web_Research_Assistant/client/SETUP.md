# Web Research Assistant - Frontend Setup

## Overview
Modern black and white themed Next.js frontend for the Web Research Assistant.

## Prerequisites
- Node.js 18+ installed
- Backend API running on `http://localhost:8000`

## Installation

1. **Install dependencies:**
```bash
npm install
```

## Running the Application

### Development Mode
```bash
npm run dev
```
The app will be available at `http://localhost:3000`

### Production Build
```bash
npm run build
npm start
```

## Features

### 🎨 Design
- **Clean black & white theme** - Minimalist, professional design
- **Fully responsive** - Works on desktop, tablet, and mobile
- **Smooth animations** - Loading states and transitions
- **Custom scrollbar** - Styled to match the theme

### 🔍 Functionality
- **Real-time research** - Submit queries and get comprehensive reports
- **Live loading states** - Visual feedback during research
- **Statistics dashboard** - View sources, pages processed, and summaries
- **Citation management** - All sources properly cited with links
- **Error handling** - Clear error messages and recovery

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/research`

**Request format:**
```
POST http://localhost:8000/research?query=YOUR_QUERY
```

**Expected response:**
```json
{
  "success": true,
  "data": {
    "query": "...",
    "sources_found": 10,
    "pages_processed": 10,
    "summaries_generated": 10,
    "report": "...",
    "citations": [...],
    "report_length": 5000,
    "timestamp": "2025-10-09 05:40:00"
  }
}
```

## Project Structure

```
client/
├── src/
│   └── app/
│       ├── page.tsx        # Main research interface
│       ├── layout.tsx      # Root layout with metadata
│       └── globals.css     # Global styles & theme
├── public/                 # Static assets
└── package.json           # Dependencies
```

## Customization

### Colors
Edit `src/app/globals.css` to change the color scheme:
```css
:root {
  --background: #ffffff;  /* Background color */
  --foreground: #000000;  /* Text color */
}
```

### API Endpoint
Edit `src/app/page.tsx` line 20 to change the backend URL:
```typescript
const response = await fetch(`YOUR_API_URL/research?query=${encodeURIComponent(query)}`, {
  method: 'POST',
});
```

## Troubleshooting

### CORS Issues
If you get CORS errors, add CORS middleware to your FastAPI backend:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Connection Refused
Make sure the backend is running on port 8000:
```bash
cd ..
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Tech Stack
- **Next.js 15** - React framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling
- **Geist Font** - Typography
