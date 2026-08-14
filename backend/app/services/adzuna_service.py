import os
import time
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
ADZUNA_COUNTRY = os.getenv("ADZUNA_COUNTRY", "gb")

BASE_URL = (
    f"https://api.adzuna.com/v1/api/jobs/"
    f"{ADZUNA_COUNTRY}/search"
)


def search_adzuna_jobs(
    role: str,
    location: str,
    minimum_salary: int | None = None,
    results_per_page: int = 5,
    page: int = 1,
) -> list[dict[str, Any]]:
    """
    Search Adzuna for live jobs and return simplified job data.
    Automatically retries temporary 503 errors.
    """

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise RuntimeError(
            "Adzuna credentials are missing from the .env file."
        )

    params: dict[str, Any] = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": role,
        "where": location,
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }

    if minimum_salary is not None:
        params["salary_min"] = minimum_salary

    maximum_attempts = 3

    for attempt in range(1, maximum_attempts + 1):

        response = requests.get(
            f"{BASE_URL}/{page}",
            params=params,
            timeout=30,
        )

        # Retry temporary Adzuna outages
        if response.status_code == 503:

            if attempt == maximum_attempts:
                response.raise_for_status()

            wait_seconds = attempt * 2

            print(
                f"Adzuna temporarily unavailable "
                f"(attempt {attempt}/{maximum_attempts}). "
                f"Retrying in {wait_seconds} seconds..."
            )

            time.sleep(wait_seconds)
            continue

        response.raise_for_status()
        break

    data = response.json()
    raw_jobs = data.get("results", [])

    jobs = []

    for job in raw_jobs:
        company = job.get("company") or {}
        job_location = job.get("location") or {}

        jobs.append(
            {
                "id": job.get("id"),
                "title": job.get("title"),
                "company": company.get(
                    "display_name",
                    "Unknown company",
                ),
                "location": job_location.get(
                    "display_name",
                    location,
                ),
                "description": job.get("description", ""),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "contract_type": job.get("contract_type"),
                "contract_time": job.get("contract_time"),
                "created": job.get("created"),
                "apply_url": job.get("redirect_url"),
                "source": "Adzuna",
            }
        )

    return jobs