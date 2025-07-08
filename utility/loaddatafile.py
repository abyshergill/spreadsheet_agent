import pandas as pd
import streamlit as st
from typing import Optional

def LoadDataFile(uploaded_file) -> Optional[pd.DataFrame]:
    try:
        if uploaded_file.name.endswith('.csv'):
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    return pd.read_csv(uploaded_file, encoding=encoding)
                except UnicodeDecodeError:
                    continue
            return pd.read_csv(uploaded_file)  
        else:
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None