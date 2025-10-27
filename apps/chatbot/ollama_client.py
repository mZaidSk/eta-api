import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"  # works inside docker


# Direct Run: http://localhost:11434


def query_ollama(prompt: str, model: str = "llama3.2") -> str:
    payload = {"model": model, "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("response", "")
