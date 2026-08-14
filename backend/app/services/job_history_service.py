import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


BACKEND_DIRECTORY = Path(__file__).resolve().parents[2]
DATABASE_DIRECTORY = BACKEND_DIRECTORY / "data"
DATABASE_PATH = DATABASE_DIRECTORY / "jobs.db"


def create_job_fingerprint(job: dict) -> str:
    """
    Create a fallback identifier using the vacancy's title,
    company and location.

    This catches reposted jobs that may receive a different
    Adzuna ID.
    """

    raw_value = "|".join(
        [
            str(job.get("title") or "").strip().lower(),
            str(job.get("company") or "").strip().lower(),
            str(job.get("location") or "").strip().lower(),
        ]
    )

    return hashlib.sha256(
        raw_value.encode("utf-8")
    ).hexdigest()


def initialise_database() -> None:
    """
    Create the database and notified_jobs table if needed.
    """

    DATABASE_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS notified_jobs (
                job_id TEXT PRIMARY KEY,
                fingerprint TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                apply_url TEXT,
                match_score INTEGER,
                notified_at TEXT NOT NULL
            )
            """
        )

        connection.commit()


def job_has_been_notified(job: dict) -> bool:
    """
    Return True when the job ID or semantic fingerprint
    already exists in the database.
    """

    initialise_database()

    job_id = str(
        job.get("id")
        or create_job_fingerprint(job)
    )

    fingerprint = create_job_fingerprint(job)

    with sqlite3.connect(DATABASE_PATH) as connection:
        result = connection.execute(
            """
            SELECT 1
            FROM notified_jobs
            WHERE job_id = ?
               OR fingerprint = ?
            LIMIT 1
            """,
            (job_id, fingerprint),
        ).fetchone()

    return result is not None


def get_new_jobs(jobs: list[dict]) -> list[dict]:
    """
    Remove jobs that have already been emailed.
    """

    return [
        job
        for job in jobs
        if not job_has_been_notified(job)
    ]


def mark_jobs_as_notified(jobs: list[dict]) -> None:
    """
    Save jobs after the notification email succeeds.
    """

    initialise_database()

    notified_at = datetime.now(
        timezone.utc
    ).isoformat()

    with sqlite3.connect(DATABASE_PATH) as connection:
        for job in jobs:
            job_id = str(
                job.get("id")
                or create_job_fingerprint(job)
            )

            fingerprint = create_job_fingerprint(job)

            connection.execute(
                """
                INSERT OR IGNORE INTO notified_jobs (
                    job_id,
                    fingerprint,
                    title,
                    company,
                    location,
                    apply_url,
                    match_score,
                    notified_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_id,
                    fingerprint,
                    job.get("title"),
                    job.get("company"),
                    job.get("location"),
                    job.get("apply_url"),
                    job.get("match_score"),
                    notified_at,
                ),
            )

        connection.commit()