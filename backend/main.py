from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes.folder_routes import router as folder_router
from app.routes.job_routes import router as job_router
from app.services.scheduler_service import (
    start_scheduler,
    stop_scheduler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()

    yield

    stop_scheduler()


app = FastAPI(
    title="PlacementAI",
    version="0.1.0",
    description=(
        "Local AI assistant for analysing a CV and finding "
        "suitable university placement vacancies."
    ),
    lifespan=lifespan,
)


app.include_router(folder_router)
app.include_router(job_router)


@app.get(
    "/",
    tags=["System"],
    summary="Check backend status",
)
def root():
    return {
        "message": "PlacementAI backend is running."
    }
    