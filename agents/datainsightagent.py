from ollama.callollama import CallOllama
import pandas as pd

def DataInsightAgent(df: pd.DataFrame, model: str) -> str:
    df_summary = f"""
Shape: {df.shape}
Columns: {list(df.columns)}
Data Types: {dict(df.dtypes)}
Missing Values: {dict(df.isnull().sum())}
Sample Data:
{df.head(3).to_string()}
"""
    
    insight_prompt = f"""Analyze this dataset and provide key insights:

{df_summary}

Provide:
1. Data quality assessment
2. Key patterns or trends you notice
3. Suggestions for analysis
4. Potential data issues

Keep response concise and actionable:"""

    return CallOllama(insight_prompt, model, temperature=0.3)