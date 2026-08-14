from apscheduler.schedulers.background import BackgroundScheduler

from app.services.scheduled_search_service import (
    run_job_search_and_notify,
)

scheduler = BackgroundScheduler()


def safe_scheduled_search():
    """
    Run the automated search without allowing an API or email
    error to permanently stop future searches.
    """

    try:
        print("\n========== AUTOMATIC JOB SEARCH ==========")

        result = run_job_search_and_notify()

        print(
            f"Searched: {result['searched_count']} | "
            f"Matched: {result['matched_count']} | "
            f"New: {result['new_count']} | "
            f"Email sent: {result['email_sent']}"
        )

        print("==========================================\n")

    except Exception as error:
        print(
            "Automatic job search failed: "
            f"{type(error).__name__}: {error}"
        )


def start_scheduler():
    """
    Start PlacementAI's automatic hourly search.
    """

    if scheduler.running:
        return

    # Run once immediately when the backend starts
    safe_scheduled_search()

    # Then continue every hour
    scheduler.add_job(
        safe_scheduled_search,
        trigger="interval",
        hours=1,
        id="placementai-hourly-job-search",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    print(
        "PlacementAI automatic job search started. "
        "Searching every hour."
    )


def stop_scheduler():
    """
    Stop the scheduler cleanly when FastAPI shuts down.
    """

    if scheduler.running:
        scheduler.shutdown(wait=False)

        print(
            "PlacementAI automatic job search stopped."
        )