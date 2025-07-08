import requests
import json

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TAGS_URL = f"{OLLAMA_BASE_URL}/api/tags"

def CheckConnection() -> bool:
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False