from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from dataclasses import dataclass


def _split_origins(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    app_env: str
    api_v1_prefix: str
    allowed_origins: list[str]
    google_api_key: str
    gemini_model: str
    youtube_api_key: str
    max_video_mb: int


_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=_env_path, override=False)

settings = Settings(
    app_env=os.getenv("APP_ENV", "local"),
    api_v1_prefix=os.getenv("API_V1_PREFIX", "/api/v1"),
    allowed_origins=_split_origins(
        os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        )
    ),
    google_api_key=os.getenv("GOOGLE_AI_STUDIO_API_KEY", "")
    or os.getenv("GEMINI_API_KEY", ""),
    gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    youtube_api_key=os.getenv("YOUTUBE_API_KEY", ""),
    max_video_mb=int(os.getenv("MAX_VIDEO_MB", "80")),
)
