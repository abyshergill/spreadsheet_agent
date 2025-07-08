import streamlit as st
import pandas as pd
import requests
import json
import traceback
import io
from typing import Optional, List, Dict, Any
import time
import re

from ollama.getmodels import GetModels
from ollama.checkconnection import CheckConnection
from ollama.callollama import CallOllama 

from worker.extractor import Extractor
from worker.validator import Validator
from worker.executor import Executor

from agents.codegenerationagent import CodeGenerationAgent
from agents.codereviewagent import CodeReviewAgent
from agents.datainsightagent import DataInsightAgent


from utility.loaddatafile import LoadDataFile
from utility.createdownloadlink import CreateDownloadLink

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"


def main():
    st.set_page_config(
        page_title="SmartSheet Agents",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🧠 SmartSheet Agents - AI-Powered Data Assistant")
    st.markdown("Transform your Excel/CSV files using natural language commands powered by local AI models.")

    with st.sidebar:
        st.header("⚙️ Configuration")
        
        if not CheckConnection():
            st.error("Ollama server not running!")
            st.markdown("Start Ollama server: `ollama serve`")
            st.stop()
        else:
            st.success("Ollama connected")

        available_models = GetModels()
        if not available_models:
            st.error("No models found. Install a model: `ollama pull llama2`")
            st.stop()
        
        selected_model = st.selectbox(
            "🤖 Select Model",
            available_models,
            help="Choose your preferred Ollama model"
        )
        
        st.markdown("---")
        
        with st.expander("🔧 Advanced Settings"):
            show_code = st.checkbox("Show Generated Code", value=True)
            show_review = st.checkbox("Show Code Review", value=True)
            auto_execute = st.checkbox("Auto-execute Approved Code", value=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload your data file",
            type=["csv", "xlsx", "xls"],
            help="Supported formats: CSV, Excel (.xlsx, .xls)"
        )
    
    if uploaded_file:
        df = LoadDataFile(uploaded_file)
        if df is None:
            st.stop()
        
        with col2:
            st.subheader("📊 Dataset Overview")
            st.write(f"**Shape:** {df.shape[0]:,} rows × {df.shape[1]} columns")
            st.write(f"**File:** {uploaded_file.name}")
        
        st.subheader("🔍 Data Preview")
        preview_rows = st.slider("Rows to preview", 5, min(50, len(df)), 10)
        st.dataframe(df.head(preview_rows), use_container_width=True)
        
        if st.button("🔍 Generate Data Insights", key="insights_btn"):
            with st.spinner("Analyzing dataset..."):
                insights = DataInsightAgent(df, selected_model)
                st.subheader("💡 Data Insights")
                st.markdown(insights)
        
        st.markdown("---")

        st.subheader("💬 What would you like to do?")
        
        example_prompts = [
            "Show summary statistics for all numeric columns",
            "Create a new column calculating the percentage of total",
            "Filter rows where values are above average",
            "Group by category and calculate totals",
            "Find and highlight missing values",
            "Create a pivot table",
            "Sort data by multiple columns"
        ]
        
        selected_example = st.selectbox(
            "📝 Quick Examples",
            ["Custom prompt..."] + example_prompts
        )
        
        if selected_example != "Custom prompt...":
            user_prompt = st.text_area(
                "Enter your request:",
                value=selected_example,
                height=100
            )
        else:
            user_prompt = st.text_area(
                "Enter your request:",
                placeholder="e.g., Add a profit column by subtracting cost from revenue",
                height=100
            )
        
        if st.button("Process Request", type="primary", disabled=not user_prompt.strip()):
            if not user_prompt.strip():
                st.warning("Please enter a request first.")
            else:
                df_info = f"""
DataFrame Shape: {df.shape}
Columns: {list(df.columns)}
Data Types:
{df.dtypes.to_string()}

Sample Data:
{df.head(3).to_string()}

Null Values: {df.isnull().sum().sum()} total
                """
                with st.spinner("🧠 Generating code..."):
                    generated_code = CodeGenerationAgent(user_prompt, df_info, selected_model)
                    clean_code = Extractor(generated_code)
                
                if not clean_code:
                    st.error("Failed to generate valid code. Please try rephrasing your request.")
                    st.stop()
                
                if show_code:
                    st.subheader("🔧 Generated Code")
                    st.code(clean_code, language="python")
                
                with st.spinner("🔍 Reviewing code..."):
                    review_result = CodeReviewAgent(clean_code, user_prompt, df_info, selected_model)
                
                if show_review:
                    st.subheader("👨‍💻 Code Review")
                    st.markdown(review_result)
                
                approved = "approved" in review_result.lower() or auto_execute
                
                if approved:
                    with st.spinner("Executing code..."):
                        new_df, error, result_var = Executor(clean_code, df)
                    
                    if error:
                        st.error(f"Execution failed:")
                        st.code(error)
                    else:
                        st.success("Code executed successfully!")
                        
                        col_result1, col_result2 = st.columns([2, 1])
                        
                        with col_result1:
                            if result_var is not None and not isinstance(result_var, pd.DataFrame):
                                st.subheader("📈 Analysis Result")
                                st.write(result_var)
                            
                            if new_df is not None and not new_df.equals(df):
                                st.subheader("📊 Updated Data")
                                st.dataframe(new_df.head(preview_rows), use_container_width=True)
                                
                                st.subheader("💾 Download Results")
                                col_dl1, col_dl2 = st.columns(2)
                                
                                with col_dl1:
                                    CreateDownloadLink(
                                        new_df, 
                                        f"processed_{uploaded_file.name.split('.')[0]}.xlsx",
                                        'excel'
                                    )
                                
                                with col_dl2:
                                    CreateDownloadLink(
                                        new_df,
                                        f"processed_{uploaded_file.name.split('.')[0]}.csv",
                                        'csv'
                                    )
                        
                        with col_result2:
                            if new_df is not None:
                                st.metric("New Shape", f"{new_df.shape[0]} × {new_df.shape[1]}")
                                if new_df.shape != df.shape:
                                    rows_diff = new_df.shape[0] - df.shape[0]
                                    cols_diff = new_df.shape[1] - df.shape[1]
                                    st.metric("Rows Changed", f"{rows_diff:+d}")
                                    st.metric("Columns Changed", f"{cols_diff:+d}")
                else:
                    st.warning("Code review suggests revisions needed. Please modify your request.")
                    if st.button("Execute Anyway", key="force_execute"):
                        with st.spinner("Executing code..."):
                            new_df, error, result_var = Executor(clean_code, df)
                        
                        if error:
                            st.error(f"Execution failed: {error}")
                        else:
                            st.success("Forced execution completed!")

if __name__ == "__main__":
    main()