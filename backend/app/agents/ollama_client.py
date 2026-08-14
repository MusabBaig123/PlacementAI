import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"


def generate_response(prompt: str) -> str:
    """
    Sends a prompt to the local Ollama model
    and returns the generated text.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    if "response" not in result:
        raise ValueError("Ollama response did not contain a 'response' field.")

    return result["response"].strip()