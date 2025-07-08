import requests
import json
import streamlit as st

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"

def CallOllama(prompt: str, model: str, temperature: float = 0.1) -> str:
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        response = requests.post(OLLAMA_GENERATE_URL, json=payload, timeout=1000)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        st.error(f"LLM Error: {str(e)}")
        return ""