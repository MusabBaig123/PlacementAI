from pydantic import BaseModel, Field


class FolderScanRequest(BaseModel):
    folder_path: str = Field(
        default=r"C:\Users\musab\Documents\PlacementAI-CV",
        min_length=1,
        description=(
            "Full local path of the folder containing the CV."
        ),
        examples=[
            r"C:\Users\musab\Documents\PlacementAI-CV"
        ],
    )