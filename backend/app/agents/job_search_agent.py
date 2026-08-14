from datetime import datetime, timezone

from app.config import JOB_PREFERENCES
from app.services.adzuna_service import search_adzuna_jobs
from app.services.profile_service import load_profile


SEARCH_TERM_MAP = {
    "Software Engineering Placement": [
        "software engineering placement",
        "software engineer internship",
        "software developer placement",
    ],
    "Backend Development Placement": [
        "backend developer placement",
        "backend engineering internship",
    ],
    "Web Development Placement": [
        "web developer placement",
        "web development internship",
    ],
    "Data Analyst Placement": [
        "data analyst placement",
        "data analyst internship",
    ],
    "AI Engineering Placement": [
        "AI placement",
        "artificial intelligence internship",
        "machine learning placement",
    ],
    "Software Testing and Automation Placement": [
        "software testing placement",
        "automation testing internship",
    ],
}


PLACEMENT_KEYWORDS = [
    "placement",
    "industrial placement",
    "industrial year",
    "year in industry",
    "intern",
    "internship",
    "undergraduate",
    "sandwich year",
]


BLOCKED_PHRASES = [
    "self-funded",
    "fees apply",
    "course fees",
    "job guarantee",
    "training programme",
    "no experience needed",
    "phd required",
    "phd or msc",
    "research scientist",
    "member of research staff",
    "quant trading",
    "quantitative trading",
    "trading internship",
    "investment banking",
    "marketing internship",
    "finance internship",
]


RELEVANT_CAREER_KEYWORDS = [
    "software",
    "developer",
    "engineering",
    "backend",
    "back-end",
    "frontend",
    "front-end",
    "web",
    "data",
    "artificial intelligence",
    "machine learning",
    "automation",
    "testing",
    "quality assurance",
    "qa",
]


def build_search_query() -> dict:
    """
    Combine the saved candidate profile with fixed job preferences.
    """

    profile = load_profile()

    preferred_roles = JOB_PREFERENCES.get(
        "desired_roles",
        [],
    )

    candidate_roles = profile.get(
        "suitable_roles",
        [],
    )

    roles = list(
        dict.fromkeys(
            preferred_roles + candidate_roles
        )
    )

    return {
        "roles": roles,
        "locations": JOB_PREFERENCES.get(
            "preferred_locations",
            [],
        ),
        "minimum_salary": JOB_PREFERENCES.get(
            "minimum_salary"
        ),
        "skills": profile.get(
            "skills",
            [],
        ),
    }


def create_search_terms(
    roles: list[str],
) -> list[str]:
    """
    Convert standard role names into phrases commonly used by
    employers and job websites.
    """

    search_terms = []

    for role in roles:
        mapped_terms = SEARCH_TERM_MAP.get(
            role,
            [role],
        )

        search_terms.extend(mapped_terms)

    return list(
        dict.fromkeys(search_terms)
    )


def has_student_job_title(
    title_lower: str,
) -> bool:
    """
    Check whether the title clearly identifies an internship,
    placement or undergraduate opportunity.
    """

    return any(
        keyword in title_lower
        for keyword in PLACEMENT_KEYWORDS
    )


def is_relevant_career_area(
    searchable_text: str,
) -> bool:
    """
    Check whether the vacancy belongs to one of the candidate's
    target technical career areas.
    """

    return any(
        keyword in searchable_text
        for keyword in RELEVANT_CAREER_KEYWORDS
    )


def is_recent_job(
    job: dict,
    maximum_age_days: int,
) -> bool:
    """
    Reject vacancies older than the permitted age.

    If the date cannot be parsed, the job is kept rather than
    rejected.
    """

    created_value = job.get("created")

    if not created_value:
        return True

    try:
        created_date = datetime.fromisoformat(
            str(created_value).replace(
                "Z",
                "+00:00",
            )
        )

        current_date = datetime.now(
            timezone.utc
        )

        age_days = (
            current_date - created_date
        ).days

        return age_days <= maximum_age_days

    except (TypeError, ValueError):
        return True


def is_placement_job(
    job: dict,
    maximum_age_days: int = 180,
) -> bool:
    """
    Keep genuine and reasonably recent technical placements
    or internships.

    Rejects:
    - roles without student-opportunity wording;
    - unrelated career areas;
    - old vacancies;
    - graduate-only roles;
    - PhD-level roles;
    - self-funded training programmes;
    - trading, finance and marketing internships.
    """

    title = str(
        job.get("title")
        or ""
    )

    description = str(
        job.get("description")
        or ""
    )

    title_lower = title.lower()

    searchable_text = (
        f"{title} {description}"
    ).lower()

    # The title must clearly describe a student opportunity.
    if not has_student_job_title(title_lower):
        return False

    # Remove unsuitable programmes and unrelated internships.
    if any(
        phrase in searchable_text
        for phrase in BLOCKED_PHRASES
    ):
        return False

    # The role must belong to a relevant technical career area.
    if not is_relevant_career_area(
        searchable_text
    ):
        return False

    # Reject graduate-only roles unless they also clearly say
    # internship or placement.
    if (
        "graduate" in title_lower
        and not any(
            keyword in title_lower
            for keyword in [
                "intern",
                "internship",
                "placement",
            ]
        )
    ):
        return False

    if not is_recent_job(
        job,
        maximum_age_days,
    ):
        return False

    return True


def create_unique_job_key(
    job: dict,
) -> object:
    """
    Create a key used to remove duplicate vacancies.

    Prefer the Adzuna ID. If no ID is present, use a normalised
    combination of title, company and location.
    """

    job_id = job.get("id")

    if job_id:
        return str(job_id)

    title = str(
        job.get("title")
        or ""
    ).strip().lower()

    company = str(
        job.get("company")
        or ""
    ).strip().lower()

    location = str(
        job.get("location")
        or ""
    ).strip().lower()

    return (
        title,
        company,
        location,
    )


def search_jobs(
    results_per_search: int = 10,
) -> list[dict]:
    """
    Search Adzuna for live technical placements and internships.

    Individual search failures are logged and skipped so that one
    failed request does not stop the whole search.
    """

    query = build_search_query()

    roles = query["roles"]
    locations = query["locations"]

    if not roles:
        raise ValueError(
            "No suitable job roles are available."
        )

    if not locations:
        locations = ["London"]

    search_terms = create_search_terms(
        roles
    )

    all_jobs = []
    failed_searches = []

    # Limit API usage while using Adzuna trial access.
    # Two search phrases across one location = two requests.
    for search_term in search_terms[:2]:
        for location in locations[:1]:
            try:
                print(
                    "Searching Adzuna: "
                    f"{search_term} in {location}"
                )

                jobs = search_adzuna_jobs(
                    role=search_term,
                    location=location,

                    # Salary is not applied during retrieval because
                    # many genuine placements omit salary information.
                    minimum_salary=None,

                    results_per_page=results_per_search,
                )

                print(
                    f"Adzuna returned {len(jobs)} jobs."
                )

                all_jobs.extend(jobs)

            except Exception as error:
                error_message = (
                    f"{search_term} in {location}: "
                    f"{type(error).__name__}: {error}"
                )

                print(
                    f"Search skipped: {error_message}"
                )

                failed_searches.append(
                    error_message
                )

    if not all_jobs and failed_searches:
        raise RuntimeError(
            "No searches completed successfully. "
            + " | ".join(failed_searches)
        )

    placement_jobs = [
        job
        for job in all_jobs
        if is_placement_job(job)
    ]

    unique_jobs = {}

    for job in placement_jobs:
        unique_key = create_unique_job_key(
            job
        )

        unique_jobs[unique_key] = job

    return list(
        unique_jobs.values()
    )