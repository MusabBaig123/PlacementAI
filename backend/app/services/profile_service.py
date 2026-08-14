import json
from pathlib import Path
from typing import Any


PROFILE_FILE = Path("candidate_profile.json")


def save_profile(profile: Any) -> None:
    """
    Save a candidate profile to a local JSON file.

    Supports either:
    - a normal Python dictionary, or
    - a Pydantic model
    """

    if hasattr(profile, "model_dump"):
        profile_data = profile.model_dump()
    elif isinstance(profile, dict):
        profile_data = profile
    else:
        raise TypeError(
            "Profile must be a dictionary or a Pydantic model."
        )

    with PROFILE_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            profile_data,
            file,
            indent=4,
            ensure_ascii=False
        )
def load_profile() -> dict:
    """
    Load the saved candidate profile.
    """

    if not PROFILE_FILE.exists():
        return {}

    with PROFILE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)