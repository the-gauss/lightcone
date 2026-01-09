from __future__ import annotations

import os
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


settings = Settings(
    app_env=os.getenv("APP_ENV", "local"),
    api_v1_prefix=os.getenv("API_V1_PREFIX", "/api/v1"),
    allowed_origins=_split_origins(
        os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        )
    ),
)
