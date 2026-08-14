import smtplib

from fastapi import APIRouter, HTTPException

from app.agents.job_search_agent import search_jobs
from app.agents.matching_agent import rank_jobs
from app.config import JOB_PREFERENCES
from app.services.email_service import send_test_email
from app.services.profile_service import load_profile
from app.services.scheduled_search_service import (
    run_job_search_and_notify,
)


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.get(
    "/search",
    summary="Search and rank live placement vacancies",
    description=(
        "Searches Adzuna for live placements, compares each job "
        "against the saved candidate profile, assigns a match "
        "score and returns the results ranked from best to worst."
    ),
)
def get_matching_jobs():
    try:
        profile = load_profile()

        jobs = search_jobs()

        ranked_jobs = rank_jobs(
            jobs=jobs,
            profile=profile,
            preferences=JOB_PREFERENCES,
            minimum_score=50,
        )

        return {
            "count": len(ranked_jobs),
            "jobs": ranked_jobs,
        }

    except (RuntimeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        error_message = (
            f"{type(error).__name__}: {error}"
        )

        print(f"Job search failed: {error_message}")

        raise HTTPException(
            status_code=502,
            detail=error_message,
        ) from error


@router.post(
    "/search-and-notify",
    summary="Search and email new matching jobs",
    description=(
        "Searches for live placements, ranks them, filters out "
        "jobs that have already been emailed, and sends an email "
        "containing only newly discovered matches."
    ),
)
def search_and_notify():
    try:
        return run_job_search_and_notify()

    except (RuntimeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        error_message = (
            f"{type(error).__name__}: {error}"
        )

        print(
            f"Search and notification failed: {error_message}"
        )

        raise HTTPException(
            status_code=502,
            detail=error_message,
        ) from error


@router.post(
    "/test-email",
    summary="Send a test notification email",
    description=(
        "Sends a test email to verify the Outlook "
        "configuration before scheduled searches are enabled."
    ),
)
def test_email():
    try:
        send_test_email()

        return {
            "message": (
                "Test email sent successfully. "
                "Check your Outlook inbox and junk folder."
            )
        }

    except smtplib.SMTPAuthenticationError as error:
     raise HTTPException(
        status_code=401,
        detail=(
            "The email provider rejected the login. "
            "Check that EMAIL_ADDRESS is the Gmail account "
            "that created the App Password and that "
            "EMAIL_PASSWORD contains the 16-character "
            "Google App Password."
        ),
    ) from error

    except smtplib.SMTPConnectError as error:
        raise HTTPException(
            status_code=502,
            detail=(
                "Could not connect to the Outlook SMTP server."
            ),
        ) from error

    except smtplib.SMTPException as error:
        error_message = (
            f"{type(error).__name__}: {error}"
        )

        print(f"SMTP email error: {error_message}")

        raise HTTPException(
            status_code=502,
            detail=error_message,
        ) from error

    except Exception as error:
        error_message = (
            f"{type(error).__name__}: {error}"
        )

        print(f"Test email failed: {error_message}")

        raise HTTPException(
            status_code=502,
            detail=error_message,
        ) from error