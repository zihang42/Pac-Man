import json
from pathlib import Path
from typing import Any, Self

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from src.logger import logger


class LevelConfig(BaseModel):
    width: int = Field(default=20, ge=10, le=99)
    height: int = Field(default=20, ge=10, le=99)


class Config(BaseModel):
    levels: list[LevelConfig] = Field(
        default_factory=lambda: [LevelConfig() for _ in range(10)],
        min_length=10,
    )
    level_max_time: int = Field(default=90, ge=10)
    lives: int = Field(default=3, ge=1, le=99)
    pacgum: int = Field(default=42, ge=1, le=999)
    points_per_pacgum: int = Field(default=10, ge=1, le=999)
    points_per_super_pacgum: int = Field(default=50, ge=1, le=999)
    points_per_ghost: int = Field(default=200, ge=1, le=999)
    highscore_filename: str = Field(default="highscore.json")
    window_width: int = Field(default=1280, ge=640)
    window_height: int = Field(default=720, ge=480)
    fps: int = Field(default=60, ge=30, le=240)
    seed: int = Field(default=42, ge=0)

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def validate_highscore(cls, highscore_filename: str) -> str:
        if Path(highscore_filename).suffix != ".json":
            raise ValueError("highscore file must be json")
        return highscore_filename

    @model_validator(mode="after")
    def validate_points(self) -> Self:
        if not (
            self.points_per_pacgum
            < self.points_per_super_pacgum
            < self.points_per_ghost
        ):
            raise ValueError(
                "points should follow pacgum < super pacgum < ghost"
            )
        return self


class Parser:
    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def load(self) -> Config:
        if not self.path.is_file():
            logger.warning("config is not a file")
            return Config()
        if not self.path.suffix == ".json":
            logger.warning("config is not a valid json")
            return Config()
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
                return self._validate(data)
        except Exception as e:
            logger.warning(f"failed to read config, {e}")
            return Config()

    def _validate(self, data: dict[str, Any]) -> Config:
        try:
            unknown_keys = set(data.keys()) - set(Config.model_fields.keys())
            for unknown_key in unknown_keys:
                logger.info(f"skip {unknown_key}")
            return Config.model_validate(data)
        except ValidationError as e:
            defaults = Config()
            data_copy = data.copy()
            for err in e.errors():
                key = str(err["loc"][0])
                data_copy[key] = getattr(defaults, key)
                logger.warning(
                    f"Invalid config field {key}, using default "
                    "value: {getattr(defaults, key)}",
                )

        return Config.model_validate(data_copy)
