from app.agents.ollama_client import generate_response


def extract_name(cv_text: str) -> str:
    prompt = f"""
Read the CV below.

Return ONLY the full name of the CV owner.
The owner's name is normally the first non-empty line.
Return exactly one name.
Do not invent names or add explanations.

CV:

{cv_text}
"""

    ai_name = generate_response(prompt)
    ai_name = ai_name.splitlines()[0].strip()

    first_line = next(
        (
            line.strip()
            for line in cv_text.splitlines()
            if line.strip()
        ),
        "",
    )

    if not ai_name or ai_name.lower() != first_line.lower():
        return first_line

    return ai_name