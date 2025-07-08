from ollama.callollama import CallOllama

def CodeReviewAgent(code: str, prompt: str, df_info: str, model: str) -> str:
    review_prompt = f"""You are a Code Review Expert. Analyze this Python code for data manipulation.

ORIGINAL REQUEST: {prompt}

DATAFRAME INFO:
{df_info}

GENERATED CODE:
{code}

REVIEW CRITERIA:
1. Does the code accomplish the user's request?
2. Is the code syntactically correct?
3. Are pandas operations used correctly?
4. Will it work with the given DataFrame structure?
5. Is it safe (no dangerous operations)?

Respond with:
- APPROVED: [Brief reason why it's good]
- NEEDS_REVISION: [Specific issues and suggestions]

REVIEW:"""

    return CallOllama(review_prompt, model, temperature=0.1)