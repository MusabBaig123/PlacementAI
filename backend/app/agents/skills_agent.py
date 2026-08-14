import re


RECOGNISED_SKILLS = [
    "Python",
    "Java",
    "SQL",
    "DHTML",
    "HTML",
    "XML",
    "CSS",
    "JavaScript",
    "React",
    "Spring Boot",
    "REST APIs",
    "H2",
    "Visual Studio 2022",
    "Git",
    "GitHub",
    "Eclipse IDE",
    "Windows",
    "Linux",
    ".NET 4.8",
    "Agile",
    "UML",
    "SSADM",
    "Object-Oriented Programming",
    "Algorithms",
    "Data Structures",
    "TCP/IP",
    "HTTP",
    "SFTP",
]


def extract_skills(skill_text: str) -> list[str]:
    """
    Extract explicitly stated technical skills using deterministic
    text matching.

    This avoids malformed JSON and invented skills from the small
    local language model.
    """

    found_skills = []

    for skill in RECOGNISED_SKILLS:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(pattern, skill_text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills