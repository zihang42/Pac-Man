"""
    This module is handling
    the import and export score
    in the json file
"""
import json
import re  # Regex B)
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

HIGHSCORE_FILE = Path("highscores.json")


class HighscoreEntry(BaseModel):
    name: str = Field(max_length=10)
    score: int = Field(ge=0)

    @field_validator('name')
    @classmethod
    def validate_name(cls, name: str) -> str:
        if not re.match(r"^[a-zA-Z0-9 ]+$", name):
            raise ValueError("Please put an alnum name !.")
        return name


class HighscoreSystem(BaseModel):
    scores: list[HighscoreEntry] = Field(default_factory=list)


def load_highscores() -> list[HighscoreEntry]:
    """
        Load the scores and name form json fiel
    """
    if not HIGHSCORE_FILE.exists():
        return []
    with open(HIGHSCORE_FILE, "r") as f:
        data = json.load(f)
    system = HighscoreSystem(scores=data.get("scores", []))
    system.scores.sort(key=lambda x: x.score, reverse=True)
    return system.scores[:10]


def save_highscores(scores: list[HighscoreEntry]) -> None:
    """
        Save 10 best player in the json
    """
    system = HighscoreSystem(scores=scores[:10])
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(system.model_dump(), f, indent=4)
