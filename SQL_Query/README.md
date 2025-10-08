# 🗄️ SQL Query Assistant

A professional AI-powered application that converts natural language questions into SQL queries and provides insights from business data using LangGraph and Streamlit.

## ✨ Features

- **Natural Language to SQL**: Convert questions like "What are the top selling products?" into SQL queries
- **Interactive Web UI**: Beautiful Streamlit interface with real-time visualizations
- **Smart Validation**: Built-in SQL safety checks and syntax validation
- **Data Visualization**: Automatic charts and graphs for query results
- **Query History**: Track and revisit previous queries
- **Professional Architecture**: Clean, modular codebase with proper separation of concerns

## 🏗️ Project Structure

```
├── src/
│   ├── core/           # Workflow and state management
│   ├── database/       # Database schema and utilities
│   ├── ui/            # Streamlit UI components
│   └── config/        # Configuration management
├── data/              # Database files and checkpoints
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd sql-query-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your Google API key
```

### 5. Run the Application

```bash
streamlit run app.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### Google API Key Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 📊 Database Schema

The application comes with a sample business database containing:

- **employees**: Company staff with salary and department information
- **products**: Product catalog with pricing and inventory data
- **customers**: Customer contact and location information
- **sales**: Transaction records linking all entities

## 💡 Example Queries

Try asking questions like:

- "What are the top 5 selling products?"
- "Which employees have the highest sales?"
- "Show me sales by department"
- "What's the average salary by department?"
- "Which customers bought the most expensive items?"
- "How many products are in each category?"
- "What's the total revenue by month?"

## 🛠️ Development

### Adding New Features

1. **UI Components**: Add new components in `src/ui/components.py`
2. **Workflow Logic**: Modify nodes in `src/core/workflow.py`
3. **Database Schema**: Update schema in `src/database/schema.py`
4. **Configuration**: Add settings in `src/config/settings.py`

### Running Tests

```bash
# Add your test commands here
python -m pytest tests/
```

## 📦 Dependencies

Key dependencies include:

- **Streamlit**: Web UI framework
- **LangGraph**: Workflow orchestration
- **LangChain**: LLM integration
- **Google Gemini**: AI model for SQL generation
- **SQLite**: Database engine
- **Plotly**: Data visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🔮 Future Enhancements

- [ ] Support for multiple databases
- [ ] Custom SQL query editor
- [ ] Export results to CSV/Excel
- [ ] Advanced visualization options
- [ ] User authentication
- [ ] Query performance analytics
- [ ] Multi-language support
