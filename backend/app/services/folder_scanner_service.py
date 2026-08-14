from pathlib import Path


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def validate_folder(folder_path: str) -> Path:
    """
    Convert the supplied text into a Path object and confirm
    that it refers to an existing folder.
    """

    folder = Path(folder_path).expanduser().resolve()

    if not folder.exists():
        raise FileNotFoundError(
            f"The folder does not exist: {folder}"
        )

    if not folder.is_dir():
        raise NotADirectoryError(
            f"The supplied path is not a folder: {folder}"
        )

    return folder


def find_cv_files(folder_path: str) -> list[Path]:
    """
    Find supported CV files directly inside the selected folder.

    Supported file types:
    - PDF
    - DOCX
    """

    folder = validate_folder(folder_path)

    cv_files = [
        file
        for file in folder.iterdir()
        if (
            file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
            and not file.name.startswith("~$")
        )
    ]

    # Show most recently modified files first.
    return sorted(
        cv_files,
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    )


def select_cv_file(folder_path: str) -> Path:
    """
    Select the CV file that should be processed.

    If only one supported file exists, use it.
    If several exist, prefer filenames containing 'cv'.
    Otherwise, use the most recently modified file.
    """

    cv_files = find_cv_files(folder_path)

    if not cv_files:
        raise FileNotFoundError(
            "No supported PDF or DOCX files were found "
            "in the selected folder."
        )

    files_named_cv = [
        file
        for file in cv_files
        if "cv" in file.stem.lower()
    ]

    if files_named_cv:
        return files_named_cv[0]

    return cv_files[0]