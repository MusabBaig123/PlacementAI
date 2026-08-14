import re


PROJECT_PATTERNS = {
    "BioTrace Sustainability Platform":
        r"BioTrace Sustainability Platform",
    "Tunnel Vision":
        r"Tunnel Vision",
    "Card Game Pontoon":
        r"Card Game Pontoon",
    "Python Calculator Project":
        r"Python Calculator(?:\s+Project)?",
}


def extract_projects(cv_text: str) -> list[str]:
    """
    Finds project titles explicitly present anywhere in the CV.

    The function uses exact pattern matching and does not ask
    the AI model to invent or rewrite project information.
    """

    normalised_text = " ".join(cv_text.split())
    projects = []

    for standard_title, pattern in PROJECT_PATTERNS.items():
        if re.search(
            pattern,
            normalised_text,
            re.IGNORECASE,
        ):
            projects.append(standard_title)

    return projects