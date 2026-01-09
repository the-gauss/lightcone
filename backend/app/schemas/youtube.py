from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl


class YouTubeRequest(BaseModel):
    url: HttpUrl = Field(..., description="YouTube URL to process")


class YouTubeResponse(BaseModel):
    status: str
    message: str
    request_id: str
    received_url: str
