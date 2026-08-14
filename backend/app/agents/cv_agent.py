import json
import re
import requests
from app.schemas.cv_schema import CVAnalysis

OLLAMA_URL = "http://localhost:11434/api/generate"


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in AI response.")

    return json.loads(match.group())


def analyse_cv(cv_text):

    prompt = f"""
You are an expert CV parser.

Extract information from the CV.

Rules:

- Return ONLY valid JSON.
- Do not explain your answer.
- Do not use markdown.
- Do not invent any information.
- If information is missing, use "" or [].

Return EXACTLY this format:

{{
    "name":"",
    "education":"",
    "skills":[],
    "projects":[],
    "experience":[],
    "suitable_roles":[]
}}

CV:

{cv_text}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()

    print("\n========== OLLAMA RESPONSE ==========")
    print(result["response"])
    print("=====================================\n")

    json_response = extract_json(result["response"])

    return CVAnalysis(**json_response)



 




