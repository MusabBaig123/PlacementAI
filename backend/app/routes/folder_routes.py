from fastapi import APIRouter, HTTPException

from app.agents.coordinator_agent import process_cv
from app.schemas.folder_scan_schema import FolderScanRequest
from app.services.cv_processing_service import extract_text
from app.services.folder_scanner_service import select_cv_file
from app.services.profile_service import save_profile


router = APIRouter(
    prefix="/cv",
    tags=["CV"],
)


@router.post(
    "/analyse-folder",
    summary="Analyse a CV from a local folder",
    description=(
        "Finds a PDF or DOCX CV in the supplied local folder, "
        "extracts its text, analyses it using the specialist agents, "
        "and saves the candidate profile."
    ),
)
def analyse_cv_from_folder(request: FolderScanRequest):
    try:
        selected_file = select_cv_file(request.folder_path)

        extracted_text = extract_text(str(selected_file))

        if not extracted_text.strip():
            raise ValueError(
                "The selected CV did not contain readable text."
            )

        result = process_cv(extracted_text)

        save_profile(result)

        return {
            "message": "CV found and analysed successfully.",
            "selected_file": selected_file.name,
            "result": result,
        }

    except (FileNotFoundError, NotADirectoryError) as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="The CV could not be analysed.",
        ) from error