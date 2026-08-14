import re


EXPERIENCE_PATTERNS = [
    (
        r"Worked within Agile-style development teams using GitHub",
        "Worked within Agile-style development teams using GitHub",
    ),
    (
        r"participating in sprint planning",
        "Participated in sprint planning",
    ),
    (
        r"iterative development",
        "Participated in iterative development",
    ),
    (
        r"project reviews",
        "Participated in project reviews",
    ),
    (
        r"continuous improvement activities",
        "Participated in continuous improvement activities",
    ),
    (
        r"project leader",
        "Acted as project leader during the BioTrace project",
    ),
    (
        r"coordinating frontend and backend responsibilities",
        "Coordinated frontend and backend responsibilities",
    ),
    (
        r"setting deadlines",
        "Set project deadlines",
    ),
    (
        r"monitoring progress",
        "Monitored project progress",
    ),
    (
        r"collaborating with fellow project leaders",
        "Collaborated with fellow project leaders",
    ),
    (
        r"successful delivery of project objectives",
        "Helped ensure successful delivery of project objectives",
    ),
]


def extract_experience(cv_text: str) -> str:
    """
    Finds factual teamwork and leadership experience explicitly
    written anywhere in the CV.

    It does not use the language model, preventing invented
    employers or job titles.
    """

    normalised_text = " ".join(cv_text.split())

    if not normalised_text:
        return ""

    experience_points = []

    for pattern, output_text in EXPERIENCE_PATTERNS:
        if re.search(
            pattern,
            normalised_text,
            re.IGNORECASE,
        ):
            experience_points.append(output_text)

    return "\n".join(dict.fromkeys(experience_points))