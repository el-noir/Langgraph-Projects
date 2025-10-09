"""
Web Research Assistant LangGraph Workflow
==========================================

This module contains the complete LangGraph workflow for conducting comprehensive
web research including search, content extraction, summarization, and report generation.
"""

# Import all required dependencies
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import WebBaseLoader
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import os
import json
import time


# Load environment variables
load_dotenv()

# Initialize global components
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)

search_tool = TavilySearch(
    max_results=10,
    topic="general"
)


# Define the workflow state schema
class ResearchState(TypedDict):
    """State schema for the research workflow"""
    query: str                          # User's research query
    search_results: List[Dict[str, Any]]  # Raw search results from Tavily
    page_contents: List[Dict[str, Any]]   # Extracted content from web pages
    summaries: List[Dict[str, str]]       # Individual page summaries
    final_report: str                     # Combined research report
    citations: List[Dict[str, str]]       # Citations and references
    error_message: Optional[str]          # Error handling


# Web Search Agent Node
def web_search_agent(state: ResearchState) -> ResearchState:
    """
    Search multiple sources using TavilySearch and return structured results
    """
    try:
        query = state["query"]
        print(f"🔍 Searching for: {query}")
        
        # Perform web search
        search_results = search_tool.invoke(query)
        
        # Extract and structure the results
        structured_results = []
        if isinstance(search_results, list):
            for result in search_results:
                structured_results.append({
                    'title': result.get('title', 'No title'),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'score': result.get('score', 0)
                })
        else:
            # Handle case where search_results is a dict with 'results' key
            results_list = search_results.get('results', [])
            for result in results_list:
                structured_results.append({
                    'title': result.get('title', 'No title'),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'score': result.get('score', 0)
                })
        
        print(f"✅ Found {len(structured_results)} search results")
        return {**state, "search_results": structured_results}
        
    except Exception as e:
        print(f"❌ Search error: {str(e)}")
        return {**state, "error_message": f"Search failed: {str(e)}"}


# Content Loader Node
def content_loader(state: ResearchState) -> ResearchState:
    """
    Extract and clean content from search result URLs using LangChain WebBaseLoader
    """
    try:
        search_results = state.get("search_results", [])
        page_contents = []
        
        print(f"📄 Loading content from {len(search_results)} pages using WebBaseLoader...")
        
        for i, result in enumerate(search_results):
            try:
                url = result.get('url', '')
                if not url:
                    continue
                    
                print(f"  Loading page {i+1}: {url[:50]}...")
                
                # Use LangChain's WebBaseLoader for robust web content extraction
                loader = WebBaseLoader(
                    web_paths=[url],
                    header_template={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    },
                    verify_ssl=False  # Handle SSL issues gracefully
                )
                
                # Load and parse the document
                documents = loader.load()
                
                if documents:
                    # Get the first document (should only be one for single URL)
                    doc = documents[0]
                    content = doc.page_content
                    
                    # Clean up the content - remove excessive whitespace
                    lines = (line.strip() for line in content.splitlines())
                    clean_content = '\n'.join(line for line in lines if line)
                    
                    # Limit content length to avoid token limits
                    if len(clean_content) > 4000:
                        clean_content = clean_content[:4000] + "..."
                    
                    page_contents.append({
                        'title': result.get('title', 'No title'),
                        'url': url,
                        'content': clean_content,
                        'original_content': result.get('content', ''),  # Keep Tavily's content as backup
                        'score': result.get('score', 0),
                        'metadata': doc.metadata  # Include metadata from loader
                    })
                    
                    print(f"    ✅ Successfully loaded {len(clean_content)} characters")
                    
                else:
                    raise Exception("No documents returned from WebBaseLoader")
                
            except Exception as e:
                print(f"  ⚠️  Failed to load {url}: {str(e)}")
                # Use Tavily's content as fallback
                fallback_content = result.get('content', 'Content not available')
                page_contents.append({
                    'title': result.get('title', 'No title'),
                    'url': result.get('url', ''),
                    'content': fallback_content,
                    'original_content': result.get('content', ''),
                    'score': result.get('score', 0),
                    'metadata': {'source': 'tavily_fallback'}
                })
                print(f"    ↳ Using Tavily fallback content ({len(fallback_content)} chars)")
            
            # Small delay to be respectful to servers
            time.sleep(0.5)
        
        print(f"✅ Loaded content from {len(page_contents)} pages")
        return {**state, "page_contents": page_contents}
        
    except Exception as e:
        print(f"❌ Content loading error: {str(e)}")
        return {**state, "error_message": f"Content loading failed: {str(e)}"}


# Document Summarizer Node
def document_summarizer(state: ResearchState) -> ResearchState:
    """
    LLM node to summarize individual documents/pages with source tracking
    """
    try:
        page_contents = state.get("page_contents", [])
        query = state.get("query", "")
        summaries = []
        
        print(f"📝 Summarizing {len(page_contents)} documents...")
        
        # Create summarization prompt
        summarize_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert research assistant. Your task is to summarize web page content 
            in relation to a specific research query. Focus on extracting the most relevant information 
            that directly addresses the research question.
            
            Guidelines:
            - Extract key facts, statistics, and insights relevant to the query
            - Maintain factual accuracy and avoid adding interpretations
            - Keep summaries concise but informative (200-300 words)
            - Include specific details like dates, numbers, names when relevant
            - If the content is not relevant to the query, mention that clearly"""),
            ("human", """Research Query: {query}
            
            Web Page Title: {title}
            Web Page URL: {url}
            
            Content to Summarize:
            {content}
            
            Please provide a focused summary of this content in relation to the research query.""")
        ])
        
        for i, page in enumerate(page_contents):
            try:
                print(f"  Summarizing page {i+1}: {page['title'][:40]}...")
                
                # Create summary using LLM
                formatted_prompt = summarize_prompt.format_messages(
                    query=query,
                    title=page['title'],
                    url=page['url'],
                    content=page['content']
                )
                
                response = model.invoke(formatted_prompt)
                summary_text = response.content
                
                summaries.append({
                    'title': page['title'],
                    'url': page['url'],
                    'summary': summary_text,
                    'score': page.get('score', 0)
                })
                
            except Exception as e:
                print(f"  ⚠️  Failed to summarize {page['title']}: {str(e)}")
                summaries.append({
                    'title': page['title'],
                    'url': page['url'],
                    'summary': f"Summary failed: {str(e)}",
                    'score': page.get('score', 0)
                })
        
        print(f"✅ Generated {len(summaries)} summaries")
        return {**state, "summaries": summaries}
        
    except Exception as e:
        print(f"❌ Summarization error: {str(e)}")
        return {**state, "error_message": f"Summarization failed: {str(e)}"}


# Report Writer Node
def report_writer(state: ResearchState) -> ResearchState:
    """
    LLM node to combine all summaries into coherent structured report
    """
    try:
        summaries = state.get("summaries", [])
        query = state.get("query", "")
        
        print(f"📊 Writing comprehensive report...")
        
        # Prepare summaries text for the prompt
        summaries_text = ""
        for i, summary in enumerate(summaries, 1):
            summaries_text += f"\n\n--- Source {i} ---\n"
            summaries_text += f"Title: {summary['title']}\n"
            summaries_text += f"URL: {summary['url']}\n"
            summaries_text += f"Summary: {summary['summary']}\n"
        
        # Create report writing prompt
        report_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert research analyst tasked with creating comprehensive, 
            well-structured research reports. Your goal is to synthesize information from multiple 
            sources into a coherent, insightful report.
            
            Report Structure:
            1. **Executive Summary** - Brief overview of key findings
            2. **Introduction** - Context and background of the research topic
            3. **Key Findings** - Main insights organized by themes/topics
            4. **Analysis** - Deeper analysis, trends, and implications
            5. **Conclusion** - Summary of main takeaways and implications
            6. **Sources** - List all sources with their URLs
            
            Guidelines:
            - Use clear, professional language
            - Organize information logically with proper headings
            - Cite sources appropriately [1], [2], etc.
            - Highlight key statistics, dates, and facts
            - Draw connections between different sources
            - Maintain objectivity and factual accuracy"""),
            ("human", """Research Query: {query}
            
            Source Summaries:
            {summaries}
            
            Please create a comprehensive research report that synthesizes all the information above 
            into a well-structured, professional document that thoroughly addresses the research query.""")
        ])
        
        # Generate the report
        formatted_prompt = report_prompt.format_messages(
            query=query,
            summaries=summaries_text
        )
        
        response = model.invoke(formatted_prompt)
        final_report = response.content
        
        print(f"✅ Generated comprehensive report ({len(final_report)} characters)")
        return {**state, "final_report": final_report}
        
    except Exception as e:
        print(f"❌ Report writing error: {str(e)}")
        return {**state, "error_message": f"Report writing failed: {str(e)}"}


# Citation Cache Node
def citation_cache(state: ResearchState) -> ResearchState:
    """
    Function to manage citations and cache results for future use
    """
    try:
        summaries = state.get("summaries", [])
        query = state.get("query", "")
        
        print(f"📚 Processing citations and caching results...")
        
        # Create structured citations
        citations = []
        for i, summary in enumerate(summaries, 1):
            citation = {
                'id': i,
                'title': summary['title'],
                'url': summary['url'],
                'access_date': time.strftime("%Y-%m-%d"),
                'relevance_score': summary.get('score', 0),
                'citation_format': f"[{i}] {summary['title']}. Retrieved {time.strftime('%Y-%m-%d')}. {summary['url']}"
            }
            citations.append(citation)
        
        # Cache the research session (in a real application, this would go to a database)
        cache_entry = {
            'query': query,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'sources_count': len(summaries),
            'citations': citations,
            'report_length': len(state.get("final_report", "")),
            'status': 'completed'
        }
        
        # In a real application, you would save this to a database or file
        print(f"✅ Cached research session with {len(citations)} citations")
        
        return {**state, "citations": citations}
        
    except Exception as e:
        print(f"❌ Citation caching error: {str(e)}")
        return {**state, "error_message": f"Citation caching failed: {str(e)}"}


# Construct LangGraph Workflow
def create_research_workflow():
    """
    Wire all nodes together in proper sequence with conditional logic
    """
    # Create the workflow graph
    workflow = StateGraph(ResearchState)
    
    # Add all nodes to the workflow
    workflow.add_node("web_search", web_search_agent)
    workflow.add_node("content_loader", content_loader)
    workflow.add_node("summarizer", document_summarizer)
    workflow.add_node("report_writer", report_writer)
    workflow.add_node("citation_cache", citation_cache)
    
    # Define the workflow edges (sequence)
    workflow.add_edge(START, "web_search")
    workflow.add_edge("web_search", "content_loader")
    workflow.add_edge("content_loader", "summarizer")
    workflow.add_edge("summarizer", "report_writer")
    workflow.add_edge("report_writer", "citation_cache")
    workflow.add_edge("citation_cache", END)
    
    # Compile the workflow with memory
    memory = MemorySaver()
    compiled_workflow = workflow.compile(checkpointer=memory)
    
    return compiled_workflow


# Streaming research function with progress updates
def run_research_stream(query: str, thread_id: str = None):
    """
    Run end-to-end research workflow with streaming progress updates
    
    Args:
        query: Research question/topic
        thread_id: Optional thread ID for session management
        
    Yields:
        Dict containing progress updates and final results
    """
    # Generate thread ID if not provided
    if thread_id is None:
        thread_id = f"research_{int(time.time())}"
    
    # Initial state
    initial_state = {
        "query": query,
        "search_results": [],
        "page_contents": [],
        "summaries": [],
        "final_report": "",
        "citations": [],
        "error_message": None
    }
    
    # Configure thread
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Yield initial status
        yield {
            "type": "status",
            "step": "initializing",
            "message": f"🔬 Starting research workflow for: '{query}'",
            "progress": 0
        }
        
        # Create workflow instance
        research_workflow = create_research_workflow()
        
        # Stream through the workflow
        step_count = 0
        total_steps = 5  # web_search, content_loader, summarizer, report_writer, citation_cache
        
        for event in research_workflow.stream(initial_state, config):
            step_count += 1
            progress = int((step_count / total_steps) * 100)
            
            # Determine which node is executing
            if "web_search" in event:
                state = event["web_search"]
                yield {
                    "type": "status",
                    "step": "searching",
                    "message": f"🔍 Searching web sources...",
                    "progress": 20,
                    "data": {
                        "sources_found": len(state.get("search_results", []))
                    }
                }
            
            elif "content_loader" in event:
                state = event["content_loader"]
                yield {
                    "type": "status",
                    "step": "loading",
                    "message": f"📄 Loading content from {len(state.get('search_results', []))} pages...",
                    "progress": 40,
                    "data": {
                        "pages_processed": len(state.get("page_contents", []))
                    }
                }
            
            elif "summarizer" in event:
                state = event["summarizer"]
                yield {
                    "type": "status",
                    "step": "summarizing",
                    "message": f"📝 Summarizing {len(state.get('page_contents', []))} documents...",
                    "progress": 60,
                    "data": {
                        "summaries_generated": len(state.get("summaries", []))
                    }
                }
            
            elif "report_writer" in event:
                state = event["report_writer"]
                yield {
                    "type": "status",
                    "step": "writing",
                    "message": "📊 Writing comprehensive report...",
                    "progress": 80,
                    "data": {
                        "report_length": len(state.get("final_report", ""))
                    }
                }
            
            elif "citation_cache" in event:
                state = event["citation_cache"]
                yield {
                    "type": "status",
                    "step": "finalizing",
                    "message": "📚 Processing citations and finalizing...",
                    "progress": 95,
                    "data": {
                        "citations_count": len(state.get("citations", []))
                    }
                }
        
        # Get final result
        final_result = research_workflow.invoke(initial_state, config)
        
        # Yield completion
        yield {
            "type": "status",
            "step": "completed",
            "message": "🎉 Research completed successfully!",
            "progress": 100
        }
        
        # Yield final result
        formatted_result = format_research_response(final_result)
        yield {
            "type": "result",
            "data": formatted_result["data"] if formatted_result["success"] else None,
            "error": formatted_result.get("error")
        }
        
    except Exception as e:
        error_msg = f"Workflow failed: {str(e)}"
        yield {
            "type": "error",
            "step": "failed",
            "message": f"❌ {error_msg}",
            "error": error_msg
        }


# Main research function
def run_research(query: str, thread_id: str = None) -> Dict[str, Any]:
    """
    Run end-to-end research workflow
    
    Args:
        query: Research question/topic
        thread_id: Optional thread ID for session management
        
    Returns:
        Dict containing research results including report, citations, etc.
    """
    print(f"🔬 Starting research workflow for: '{query}'")
    print("=" * 60)
    
    # Generate thread ID if not provided
    if thread_id is None:
        thread_id = f"research_{int(time.time())}"
    
    # Initial state
    initial_state = {
        "query": query,
        "search_results": [],
        "page_contents": [],
        "summaries": [],
        "final_report": "",
        "citations": [],
        "error_message": None
    }
    
    # Configure thread
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Create workflow instance
        research_workflow = create_research_workflow()
        
        # Run the workflow
        result = research_workflow.invoke(initial_state, config)
        
        print("\n" + "=" * 60)
        print("🎉 RESEARCH COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        return result
        
    except Exception as e:
        error_msg = f"Workflow failed: {str(e)}"
        print(f"\n❌ {error_msg}")
        return {
            **initial_state,
            "error_message": error_msg
        }


# Utility functions for API responses
def format_research_response(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format research results for API response"""
    if not result:
        return {
            "success": False,
            "error": "No research results available",
            "data": None
        }
    
    if result.get("error_message"):
        return {
            "success": False,
            "error": result["error_message"],
            "data": None
        }
    
    return {
        "success": True,
        "error": None,
        "data": {
            "query": result.get("query", ""),
            "sources_found": len(result.get("search_results", [])),
            "pages_processed": len(result.get("page_contents", [])),
            "summaries_generated": len(result.get("summaries", [])),
            "report": result.get("final_report", ""),
            "citations": result.get("citations", []),
            "report_length": len(result.get("final_report", "")),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }


if __name__ == "__main__":
    # Test the workflow
    test_query = "Latest developments in renewable energy 2024"
    result = run_research(test_query)
    formatted_result = format_research_response(result)
    print(f"\n📊 Research completed. Success: {formatted_result['success']}")
    if formatted_result['success']:
        print(f"Report length: {formatted_result['data']['report_length']} characters")