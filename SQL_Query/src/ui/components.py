import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional
import plotly.express as px
import plotly.graph_objects as go

def display_query_results(results: List[Dict[str, Any]], max_display: int = 100):
    """
    Display query results in a formatted table with optional charts
    """
    if not results:
        st.warning("No results found for your query.")
        return
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(results)
    
    # Display basic info
    st.success(f"✅ Query executed successfully! Found {len(results)} result(s)")
    
    # Show results in a table
    if len(results) <= max_display:
        st.dataframe(df, use_container_width=True)
    else:
        st.dataframe(df.head(max_display), use_container_width=True)
        st.info(f"Showing first {max_display} results out of {len(results)} total results.")
    
    # Try to create visualizations for numeric data
    create_visualizations(df)

def create_visualizations(df: pd.DataFrame):
    """
    Create automatic visualizations based on the data
    """
    if df.empty:
        return
    
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) == 0:
        return
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["📊 Charts", "📈 Trends", "📋 Summary"])
    
    with tab1:
        # Bar chart for categorical data
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if categorical_cols and numeric_cols:
            col1, col2 = st.columns(2)
            
            with col1:
                cat_col = st.selectbox("Select category", categorical_cols, key="cat_col")
            with col2:
                num_col = st.selectbox("Select metric", numeric_cols, key="num_col")
            
            if cat_col and num_col:
                # Group by category and sum numeric values
                grouped = df.groupby(cat_col)[num_col].sum().reset_index()
                
                fig = px.bar(
                    grouped, 
                    x=cat_col, 
                    y=num_col,
                    title=f"{num_col} by {cat_col}",
                    color=num_col,
                    color_continuous_scale='viridis'
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Time series if date column exists
        date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        
        if date_cols and numeric_cols:
            date_col = st.selectbox("Select date column", date_cols, key="date_col")
            metric_col = st.selectbox("Select metric", numeric_cols, key="metric_col")
            
            if date_col and metric_col:
                try:
                    # Convert to datetime
                    df_temp = df.copy()
                    df_temp[date_col] = pd.to_datetime(df_temp[date_col])
                    df_temp = df_temp.sort_values(date_col)
                    
                    fig = px.line(
                        df_temp, 
                        x=date_col, 
                        y=metric_col,
                        title=f"{metric_col} over time"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("Could not create time series chart with selected columns.")
    
    with tab3:
        # Summary statistics
        st.subheader("📊 Summary Statistics")
        
        if numeric_cols:
            summary_stats = df[numeric_cols].describe()
            st.dataframe(summary_stats, use_container_width=True)
        
        # Data types info
        st.subheader("📋 Data Information")
        info_data = {
            'Column': df.columns.tolist(),
            'Data Type': [str(dtype) for dtype in df.dtypes],
            'Non-Null Count': df.count().tolist(),
            'Null Count': df.isnull().sum().tolist()
        }
        info_df = pd.DataFrame(info_data)
        st.dataframe(info_df, use_container_width=True)

def display_sql_query(sql_query: str):
    """
    Display the generated SQL query in a formatted code block
    """
    st.subheader("🔍 Generated SQL Query")
    st.code(sql_query, language="sql")

def display_error_message(error_message: str):
    """
    Display error messages in a user-friendly format
    """
    st.error(f"❌ {error_message}")

def display_workflow_status(status: str, step: str):
    """
    Display workflow execution status
    """
    if status == "success":
        st.success(f"✅ {step}")
    elif status == "error":
        st.error(f"❌ {step}")
    elif status == "warning":
        st.warning(f"⚠️ {step}")
    else:
        st.info(f"ℹ️ {step}")

def create_sidebar():
    """
    Create the sidebar with database info and examples
    """
    with st.sidebar:
        st.header("🗄️ Database Info")
        
        # Database schema info
        st.subheader("Available Tables")
        tables_info = {
            "employees": "Company staff with salary and department info",
            "products": "Product catalog with pricing and inventory",
            "customers": "Customer contact and location data",
            "sales": "Transaction records linking all entities"
        }
        
        for table, description in tables_info.items():
            with st.expander(f"📋 {table}"):
                st.write(description)
        
        st.subheader("💡 Example Queries")
        example_queries = [
            "What are the top 5 selling products?",
            "Which employees have the highest sales?",
            "Show me sales by department",
            "What's the average salary by department?",
            "Which customers bought the most expensive items?",
            "How many products are in each category?",
            "What's the total revenue by month?",
            "Which products are low in stock?"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{hash(query)}"):
                st.session_state.example_query = query
                st.rerun()

def display_loading_spinner(message: str = "Processing your request..."):
    """
    Display a loading spinner with custom message
    """
    return st.spinner(message)

def create_header():
    """
    Create the main header for the application
    """
    st.set_page_config(
        page_title="SQL Query Assistant",
        page_icon="🗄️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main header
    st.title("🗄️ SQL Query Assistant")
    st.markdown("**Ask questions about your business data in natural language**")
    
    # Description
    st.markdown("""
    This AI-powered assistant converts your natural language questions into SQL queries 
    and provides insights from your business database. Simply ask questions like 
    "What are the top selling products?" and get instant answers with visualizations.
    """)
    
    st.divider()

def display_final_response(response: str):
    """
    Display the final AI response in a formatted way
    """
    st.subheader("🤖 AI Analysis")
    st.markdown(response)
