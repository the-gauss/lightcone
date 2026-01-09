from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.schemas.youtube import YouTubeRequest, YouTubeResponse
from backend.app.services.youtube import enqueue_youtube_processing

router = APIRouter()


@router.post("/process", response_model=YouTubeResponse)
def process_youtube(payload: YouTubeRequest) -> YouTubeResponse:
    url = str(payload.url)
    if "youtube.com" not in url and "youtu.be" not in url:
        raise HTTPException(status_code=400, detail="URL must be a YouTube link")

    job_id = enqueue_youtube_processing(url)
    return YouTubeResponse(
        status="queued",
        message="Video queued for processing",
        request_id=job_id,
        received_url=url,
    )
