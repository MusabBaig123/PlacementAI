import re
from datetime import datetime, timezone
from typing import Any


ROLE_KEYWORDS = {
    "software": [
        "software engineer",
        "software engineering",
        "software developer",
        "application developer",
    ],
    "backend": [
        "backend",
        "back-end",
        "server-side",
        "api developer",
    ],
    "frontend": [
        "frontend",
        "front-end",
        "ui engineer",
        "web developer",
        "react developer",
    ],
    "data": [
        "data analyst",
        "data engineer",
        "business intelligence",
        "analytics",
    ],
    "ai": [
        "artificial intelligence",
        "machine learning",
        "ai engineer",
        "ml engineer",
    ],
    "testing": [
        "software tester",
        "quality assurance",
        "qa engineer",
        "test automation",
        "automation engineer",
    ],
}


KNOWN_TECHNICAL_SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "React",
    "Spring Boot",
    "FastAPI",
    "SQL",
    "H2",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "REST API",
    "REST APIs",
    "Git",
    "GitHub",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "Linux",
    "HTML",
    "CSS",
    "Agile",
    "UML",
    "Data Structures",
    "Algorithms",
    "Machine Learning",
    "Artificial Intelligence",
    "C++",
    "C#",
    ".NET",
]


STUDENT_KEYWORDS = [
    "intern",
    "internship",
    "placement",
    "industrial placement",
    "year in industry",
    "sandwich year",
    "undergraduate",
]


def normalise_text(value: Any) -> str:
    """
    Convert a value to lowercase searchable text.
    """

    return str(value or "").strip().lower()


def skill_appears_in_text(
    skill: str,
    text: str,
) -> bool:
    """
    Match a complete skill term instead of matching it inside
    an unrelated word.

    For example, 'Git' should not match part of a longer word.
    """

    pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

    return bool(
        re.search(
            pattern,
            text,
            re.IGNORECASE,
        )
    )


def is_relevant_role(job: dict) -> bool:
    """
    Check whether the job title belongs to one of the candidate's
    target technical career areas.
    """

    title = normalise_text(job.get("title"))

    allowed_keywords = [
        keyword
        for keyword_group in ROLE_KEYWORDS.values()
        for keyword in keyword_group
    ]

    return any(
        keyword in title
        for keyword in allowed_keywords
    )


def find_matching_skills(
    job: dict,
    candidate_skills: list[str],
) -> list[str]:
    """
    Find candidate skills explicitly mentioned in the job title
    or description.
    """

    job_text = (
        f"{job.get('title', '')} "
        f"{job.get('description', '')}"
    )

    matching_skills = []

    for skill in candidate_skills:
        if skill_appears_in_text(skill, job_text):
            matching_skills.append(skill)

    return list(dict.fromkeys(matching_skills))


def find_missing_skills(
    job: dict,
    candidate_skills: list[str],
) -> list[str]:
    """
    Find recognised technical skills mentioned in the vacancy
    that are not present in the candidate profile.
    """

    job_text = (
        f"{job.get('title', '')} "
        f"{job.get('description', '')}"
    )

    candidate_skill_names = {
        normalise_text(skill)
        for skill in candidate_skills
    }

    missing_skills = []

    for skill in KNOWN_TECHNICAL_SKILLS:
        normalised_skill = normalise_text(skill)

        if (
            skill_appears_in_text(skill, job_text)
            and normalised_skill not in candidate_skill_names
        ):
            missing_skills.append(skill)

    return list(dict.fromkeys(missing_skills))


def calculate_role_score(
    job: dict,
    suitable_roles: list[str],
) -> int:
    """
    Award up to 35 points based on how closely the title
    matches the candidate's suitable roles.
    """

    title = normalise_text(job.get("title"))

    direct_role_words = []

    for role in suitable_roles:
        cleaned_role = (
            normalise_text(role)
            .replace("placement", "")
            .replace("internship", "")
            .replace("intern", "")
            .strip()
        )

        if cleaned_role:
            direct_role_words.append(cleaned_role)

    if any(
        role_word in title
        for role_word in direct_role_words
    ):
        return 35

    for keywords in ROLE_KEYWORDS.values():
        if any(
            keyword in title
            for keyword in keywords
        ):
            return 25

    return 0


def calculate_skill_score(
    matching_skills: list[str],
) -> int:
    """
    Give more weight to genuine technical-skill overlap.
    Maximum score: 30 points.
    """

    if not matching_skills:
        return 0

    if len(matching_skills) == 1:
        return 8

    if len(matching_skills) == 2:
        return 16

    if len(matching_skills) == 3:
        return 24

    return 30


def calculate_student_score(job: dict) -> int:
    """
    Award 15 points when the job title clearly identifies
    the role as an internship or placement.
    """

    title = normalise_text(job.get("title"))

    if any(
        keyword in title
        for keyword in STUDENT_KEYWORDS
    ):
        return 15

    return 0


def calculate_location_score(
    job: dict,
    preferred_locations: list[str],
) -> int:
    """
    Award 10 points when the vacancy matches a preferred location.
    """

    job_location = normalise_text(
        job.get("location")
    )

    for location in preferred_locations:
        if normalise_text(location) in job_location:
            return 10

    return 0


def calculate_recency_score(job: dict) -> int:
    """
    Award up to five points based on how recently the vacancy
    was created.
    """

    created_value = job.get("created")

    if not created_value:
        return 0

    try:
        created_date = datetime.fromisoformat(
            str(created_value).replace(
                "Z",
                "+00:00",
            )
        )

        age_days = (
            datetime.now(timezone.utc)
            - created_date
        ).days

        if age_days <= 30:
            return 5

        if age_days <= 90:
            return 3

        if age_days <= 180:
            return 1

    except (TypeError, ValueError):
        return 0

    return 0


def create_recommendation(
    score: int,
    matching_skills: list[str],
) -> str:
    """
    Explain the recommendation using only evidence found
    in the vacancy.
    """

    if (
        score >= 80
        and len(matching_skills) >= 2
    ):
        level = "Excellent match"

    elif (
        score >= 65
        and matching_skills
    ):
        level = "Strong match"

    elif score >= 50:
        level = "Possible match"

    else:
        level = "Weak match"

    if matching_skills:
        skills_text = ", ".join(
            matching_skills[:5]
        )

        return (
            f"{level}. The vacancy explicitly mentions "
            f"skills from your profile: {skills_text}."
        )

    return (
        f"{level}. The role title, student eligibility and "
        f"location match your preferences, but no clear "
        f"technical-skill overlap was found in the available "
        f"description."
    )


def score_job(
    job: dict,
    profile: dict,
    preferences: dict,
) -> dict | None:
    """
    Score one vacancy against the candidate profile.

    Returns None for unrelated roles.
    """

    if not is_relevant_role(job):
        return None

    candidate_skills = profile.get(
        "skills",
        [],
    )

    suitable_roles = profile.get(
        "suitable_roles",
        [],
    )

    preferred_locations = preferences.get(
        "preferred_locations",
        [],
    )

    matching_skills = find_matching_skills(
        job,
        candidate_skills,
    )

    missing_skills = find_missing_skills(
        job,
        candidate_skills,
    )

    role_score = calculate_role_score(
        job,
        suitable_roles,
    )

    skill_score = calculate_skill_score(
        matching_skills,
    )

    student_score = calculate_student_score(job)

    location_score = calculate_location_score(
        job,
        preferred_locations,
    )

    recency_score = calculate_recency_score(job)

    total_score = (
        role_score
        + skill_score
        + student_score
        + location_score
        + recency_score
    )

    # Do not label a vacancy as a strong match when no
    # technical skills from the candidate profile appear.
    if not matching_skills:
        total_score = min(
            total_score,
            59,
        )

    scored_job = dict(job)

    scored_job.update(
        {
            "match_score": total_score,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "score_breakdown": {
                "role": role_score,
                "skills": skill_score,
                "student_eligibility": (
                    student_score
                ),
                "location": location_score,
                "recency": recency_score,
            },
            "recommendation": (
                create_recommendation(
                    total_score,
                    matching_skills,
                )
            ),
        }
    )

    return scored_job


def rank_jobs(
    jobs: list[dict],
    profile: dict,
    preferences: dict,
    minimum_score: int = 50,
) -> list[dict]:
    """
    Score every job, remove weak or unrelated matches and sort
    the remaining vacancies from highest to lowest score.
    """

    ranked_jobs = []

    for job in jobs:
        scored_job = score_job(
            job,
            profile,
            preferences,
        )

        if (
            scored_job is not None
            and scored_job["match_score"]
            >= minimum_score
        ):
            ranked_jobs.append(scored_job)

    return sorted(
        ranked_jobs,
        key=lambda item: item[
            "match_score"
        ],
        reverse=True,
    )