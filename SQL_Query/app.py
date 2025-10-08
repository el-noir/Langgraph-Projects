import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.workflow import create_sql_workflow, SQLWorkflowState
from src.database.schema import create_sample_database, get_schema_description
from src.ui.components import (
    create_header, create_sidebar, display_query_results, 
    display_sql_query, display_error_message, display_final_response,
    display_loading_spinner
)
from src.config.settings import settings

def initialize_database():
    """Initialize the sample database if it doesn't exist"""
    if not settings.DATABASE_PATH.exists():
        with st.spinner("Creating sample database..."):
            create_sample_database()
            st.success("✅ Sample database created successfully!")

def main():
    """Main application function"""
    
    # Create header and sidebar
    create_header()
    create_sidebar()
    
    # Initialize database
    initialize_database()
    
    # Initialize session state
    if "workflow_results" not in st.session_state:
        st.session_state.workflow_results = None
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    
    # Main input area
    st.subheader("💬 Ask a Question")
    
    # Check for example query from sidebar
    if "example_query" in st.session_state:
        default_query = st.session_state.example_query
        del st.session_state.example_query
    else:
        default_query = ""
    
    # Text input for user question
    user_question = st.text_area(
        "Enter your question about the business data:",
        value=default_query,
        height=100,
        placeholder="e.g., What are the top 5 selling products?",
        help="Ask questions about employees, products, customers, or sales data."
    )
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.button("🚀 Execute Query", type="primary", use_container_width=True)
    
    # Process the query
    if submit_button and user_question.strip():
        
        # Create workflow
        try:
            workflow = create_sql_workflow()
            
            # Prepare initial state
            initial_state = SQLWorkflowState(
                user_question=user_question.strip(),
                generated_sql=None,
                sql_validation_error=None,
                query_results=None,
                final_response=None,
                error_message=None,
                database_schema=None
            )
            
            # Execute workflow with progress tracking
            with display_loading_spinner("Processing your question..."):
                result = workflow.invoke(initial_state)
            
            # Store results in session state
            st.session_state.workflow_results = result
            
            # Add to query history
            st.session_state.query_history.append({
                "question": user_question.strip(),
                "sql": result.get("generated_sql", ""),
                "results_count": len(result.get("query_results", [])),
                "success": not bool(result.get("error_message") or result.get("sql_validation_error"))
            })
            
        except Exception as e:
            st.error(f"❌ Failed to initialize workflow: {str(e)}")
            return
    
    # Display results if available
    if st.session_state.workflow_results:
        result = st.session_state.workflow_results
        
        # Display SQL query
        if result.get("generated_sql"):
            display_sql_query(result["generated_sql"])
        
        # Display error messages
        if result.get("error_message"):
            display_error_message(result["error_message"])
        elif result.get("sql_validation_error"):
            display_error_message(result["sql_validation_error"])
        
        # Display query results
        if result.get("query_results") is not None:
            display_query_results(result["query_results"])
        
        # Display final AI response
        if result.get("final_response"):
            display_final_response(result["final_response"])
    
    # Query history section
    if st.session_state.query_history:
        st.divider()
        st.subheader("📚 Query History")
        
        # Show last 5 queries
        recent_queries = st.session_state.query_history[-5:]
        
        for i, query_info in enumerate(reversed(recent_queries)):
            with st.expander(f"Query {len(st.session_state.query_history) - i}: {query_info['question'][:50]}..."):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Question:** {query_info['question']}")
                    if query_info['sql']:
                        st.code(query_info['sql'], language="sql")
                
                with col2:
                    if query_info['success']:
                        st.success(f"✅ {query_info['results_count']} results")
                    else:
                        st.error("❌ Failed")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit, LangGraph, and Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        # Validate configuration
        settings.validate_config()
        main()
    except Exception as e:
        st.error(f"❌ Application Error: {str(e)}")
        st.info("Please check your configuration and try again.")
