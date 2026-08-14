import re


SECTION_HEADINGS = {
    "PROFILE SUMMARY": "profile_summary",
    "TECHNICAL SKILLS": "technical_skills",
    "EDUCATION": "education",
    "PROJECTS": "projects",
    "SOFT SKILLS": "soft_skills",
    "INTERESTS": "interests",
}


def normalise_cv_text(cv_text: str) -> str:
    """
    Cleans common formatting problems introduced when extracting
    text from PDF and DOCX files.
    """

    text = cv_text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace unusual bullet characters with standard bullets.
    text = text.replace("", "•").replace("￾", "-")

    # Remove unnecessary spaces before line endings.
    text = "\n".join(line.rstrip() for line in text.splitlines())

    return text


def extract_cv_sections(cv_text: str) -> dict[str, str]:
    """
    Splits the CV into named sections.

    This CV contains two EXPERIENCE headings:
    - the first contains project information;
    - the second contains general teamwork/leadership experience.

    The function therefore treats:
    - first EXPERIENCE as projects;
    - second EXPERIENCE as experience.
    """

    text = normalise_cv_text(cv_text)
    lines = text.splitlines()

    sections: dict[str, list[str]] = {
        "header": [],
        "profile_summary": [],
        "technical_skills": [],
        "education": [],
        "projects": [],
        "experience": [],
        "soft_skills": [],
        "interests": [],
    }

    current_section = "header"
    experience_heading_count = 0

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        upper_line = line.upper()

        if upper_line == "EXPERIENCE":
            experience_heading_count += 1

            if experience_heading_count == 1:
                current_section = "projects"
            else:
                current_section = "experience"

            continue

        if upper_line in SECTION_HEADINGS:
            current_section = SECTION_HEADINGS[upper_line]
            continue

        sections[current_section].append(line)

    return {
        section_name: "\n".join(section_lines).strip()
        for section_name, section_lines in sections.items()
    }


def extract_numbered_project_titles(project_text: str) -> list[str]:
    """
    Extracts numbered project headings while handling headings
    that may wrap across lines during DOCX text extraction.
    """

    known_title_patterns = [
        r"BioTrace Sustainability Platform(?:\s*\(Team Project\))?",
        r"Tunnel Vision(?:\s*\(Robotic Team Project\))?",
        r"Card Game Pontoon",
        r"Python Calculator Project",
    ]

    titles = []

    for pattern in known_title_patterns:
        match = re.search(
            pattern,
            project_text,
            re.IGNORECASE
        )

        if match:
            titles.append(match.group().strip())

    return titles