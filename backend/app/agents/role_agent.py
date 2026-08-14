import re

from app.agents.ollama_client import generate_response


def extract_quoted_roles(text: str) -> list[str]:
    """
    Extracts quoted values from valid or malformed model output.
    """

    return [
        value.strip()
        for value in re.findall(r'"([^"]+)"', text)
        if value.strip()
    ]


def is_valid_role(role: str) -> bool:
    """
    Rejects dates, months and unsuitable senior roles.
    """

    blocked_terms = [
        "senior",
        "principal",
        "director",
        "head of",
        "manager",
        "management",
        "lead developer",
    ]

    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]

    lower_role = role.lower()

    if any(term in lower_role for term in blocked_terms):
        return False

    if any(month in lower_role for month in months):
        return False

    if re.search(r"\b(19|20)\d{2}\b", role):
        return False

    role_keywords = [
        "placement",
        "intern",
        "internship",
        "engineer",
        "developer",
        "analyst",
        "tester",
        "data science",
        "automation",
    ]

    return any(keyword in lower_role for keyword in role_keywords)


def normalise_role(role: str) -> str:
    replacements = {
        "Software Engineer": "Software Engineering Placement",
        "Software Engineer Placement": "Software Engineering Placement",
        "Backend Developer": "Backend Development Placement",
        "Backend Developer Placement": "Backend Development Placement",
        "Web Developer": "Web Development Placement",
        "Web Developer Placement": "Web Development Placement",
        "Data Analyst": "Data Analyst Placement",
        "Artificial Intelligence Developer": "AI Engineering Placement",
        "AI Data Engineer": "AI/Data Engineering Placement",
        "Testing Engineer": "Software Testing Placement",
        "Automation Tester": "Software Testing and Automation Placement",
        "Artificial Intelligence Engineer": "AI Engineering Placement",
    }

    cleaned_role = role.strip()

    return replacements.get(cleaned_role, cleaned_role)


def suggest_roles(candidate_summary: str) -> list[str]:
    prompt = f"""
Based only on this candidate profile, return a JSON array
containing between 3 and 6 suitable 12-month industrial
placement roles.

Suggest roles related to:
- software engineering;
- backend development;
- web development;
- data;
- artificial intelligence;
- testing and automation.

Do not include dates, months, application dates or start dates.
Do not suggest senior or management positions.
Do not include explanations or markdown.

Candidate profile:

{candidate_summary}
"""

    ai_response = generate_response(prompt)

    print("\n========== ROLE AGENT RESPONSE ==========")
    print(ai_response)
    print("=========================================\n")

    extracted_roles = extract_quoted_roles(ai_response)

    valid_roles = [
        normalise_role(role)
        for role in extracted_roles
        if is_valid_role(role)
    ]

    return list(dict.fromkeys(valid_roles))[:6]