import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


EMAIL_HOST = os.getenv(
    "EMAIL_HOST",
    "smtp-mail.outlook.com",
)

EMAIL_PORT = int(
    os.getenv("EMAIL_PORT", "587")
)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")


def validate_email_configuration() -> None:
    """
    Check that all required email settings exist.
    """

    missing_settings = []

    if not EMAIL_ADDRESS:
        missing_settings.append("EMAIL_ADDRESS")

    if not EMAIL_PASSWORD:
        missing_settings.append("EMAIL_PASSWORD")

    if not EMAIL_RECIPIENT:
        missing_settings.append("EMAIL_RECIPIENT")

    if missing_settings:
        raise RuntimeError(
            "Missing email configuration: "
            + ", ".join(missing_settings)
        )


def create_email_body(jobs: list[dict]) -> str:
    """
    Build the text displayed in the notification email.
    """

    lines = [
        f"PlacementAI found {len(jobs)} new matching role(s).",
        "",
    ]

    for index, job in enumerate(jobs, start=1):
        matching_skills = job.get(
            "matching_skills",
            [],
        )

        missing_skills = job.get(
            "missing_skills",
            [],
        )

        lines.extend(
            [
                f"{index}. {job.get('title', 'Unknown role')}",
                f"Company: {job.get('company', 'Unknown')}",
                f"Location: {job.get('location', 'Unknown')}",
                f"Match score: {job.get('match_score', 0)}%",
                (
                    "Matching skills: "
                    + (
                        ", ".join(matching_skills)
                        if matching_skills
                        else "No explicit skill matches found"
                    )
                ),
                (
                    "Skills to develop: "
                    + (
                        ", ".join(missing_skills[:5])
                        if missing_skills
                        else "None identified"
                    )
                ),
                f"Reason: {job.get('recommendation', '')}",
                f"Apply: {job.get('apply_url', '')}",
                "",
                "-" * 60,
                "",
            ]
        )

    return "\n".join(lines)


def send_job_notification(jobs: list[dict]) -> None:
    """
    Send an Outlook email containing newly found jobs.
    """

    if not jobs:
        return

    validate_email_configuration()

    message = EmailMessage()

    message["Subject"] = (
        f"PlacementAI found {len(jobs)} new job match(es)"
    )

    message["From"] = EMAIL_ADDRESS
    message["To"] = EMAIL_RECIPIENT

    message.set_content(
        create_email_body(jobs)
    )

    with smtplib.SMTP(
        EMAIL_HOST,
        EMAIL_PORT,
        timeout=30,
    ) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD,
        )

        smtp.send_message(message)


def send_test_email() -> None:
    """
    Send a simple test email without searching for jobs.
    """

    test_job = {
        "title": "PlacementAI Email Test",
        "company": "PlacementAI",
        "location": "Test",
        "match_score": 100,
        "matching_skills": [
            "Python",
            "FastAPI",
        ],
        "missing_skills": [],
        "recommendation": (
            "Your PlacementAI email service is working."
        ),
        "apply_url": "No application link - this is a test.",
    }

    send_job_notification([test_job])