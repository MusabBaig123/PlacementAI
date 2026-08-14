from app.agents.job_search_agent import search_jobs
from app.agents.matching_agent import rank_jobs
from app.config import JOB_PREFERENCES
from app.services.email_service import (
    send_job_notification,
)
from app.services.job_history_service import (
    get_new_jobs,
    mark_jobs_as_notified,
)
from app.services.profile_service import load_profile


MINIMUM_NOTIFICATION_SCORE = 60


def run_job_search_and_notify() -> dict:
    """
    Search, rank, deduplicate and email newly discovered jobs.
    """

    print("Starting scheduled PlacementAI job search...")

    profile = load_profile()
    searched_jobs = search_jobs()

    ranked_jobs = rank_jobs(
        jobs=searched_jobs,
        profile=profile,
        preferences=JOB_PREFERENCES,
        minimum_score=MINIMUM_NOTIFICATION_SCORE,
    )

    new_jobs = get_new_jobs(ranked_jobs)

    if not new_jobs:
        print(
            "No new matching jobs were found. "
            "No email was sent."
        )

        return {
            "searched_count": len(searched_jobs),
            "matched_count": len(ranked_jobs),
            "new_count": 0,
            "email_sent": False,
            "jobs": [],
        }

    send_job_notification(new_jobs)

    # Only store jobs after the email succeeds.
    mark_jobs_as_notified(new_jobs)

    print(
        f"Email sent with {len(new_jobs)} new jobs."
    )

    return {
        "searched_count": len(searched_jobs),
        "matched_count": len(ranked_jobs),
        "new_count": len(new_jobs),
        "email_sent": True,
        "jobs": new_jobs,
    }