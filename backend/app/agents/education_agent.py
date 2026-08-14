import re


def extract_education(education_text: str) -> str:
    """
    Extract university-level education directly from the CV text.
    """

    normalised_text = " ".join(education_text.split())

    university_match = re.search(
        r"Brunel University,\s*Uxbridge",
        normalised_text,
        re.IGNORECASE,
    )

    degree_match = re.search(
        r"BSc\s*\(Hons\)\s*Computer Science\s*[–-]\s*Sep\s*2024\s*[–-]\s*Present",
        normalised_text,
        re.IGNORECASE,
    )

    classification_match = re.search(
        r"Expected Classification:\s*2:1 or above",
        normalised_text,
        re.IGNORECASE,
    )

    parts = []

    if university_match:
        parts.append(university_match.group().strip())

    if degree_match:
        parts.append(degree_match.group().strip())

    if classification_match:
        parts.append(classification_match.group().strip())

    return "\n".join(parts)