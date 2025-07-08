import requests
import json
from typing import List

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"

def GetModels() -> List[str]:
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=10)
        if response.status_code == 200:
            models_data = response.json()
            return [model['name'] for model in models_data.get('models', [])]
        return []
    except requests.exceptions.RequestException:
        return []
