from ollama.callollama import CallOllama

def CodeGenerationAgent(prompt: str, df_info: str, model: str) -> str:
    system_prompt = f"""You are a Python Data Analysis Expert specializing in pandas operations.

DATAFRAME INFO:
{df_info}

USER REQUEST: {prompt}

INSTRUCTIONS:
1. Generate ONLY Python code that accomplishes the user's request
2. The DataFrame is already loaded as 'df'
3. Use pandas operations efficiently
4. Include comments for complex operations
5. DO NOT include explanations outside the code
6. Ensure code is safe (no file operations, imports, etc.)
7. Return result in 'df' variable or create 'result' variable for outputs

Example formats:
- For modifications: df['new_column'] = df['col1'] + df['col2']
- For analysis: result = df.groupby('category').sum()
- For filtering: df = df[df['column'] > 100]

GENERATE PYTHON CODE ONLY:"""

    return CallOllama(system_prompt, model, temperature=0.1)