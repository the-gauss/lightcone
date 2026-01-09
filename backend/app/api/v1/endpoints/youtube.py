from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.schemas.youtube import YouTubeRequest, YouTubeResponse
from backend.app.services.youtube import run_youtube_workflow

router = APIRouter()


@router.post("/process", response_model=YouTubeResponse)
def process_youtube_endpoint(payload: YouTubeRequest) -> YouTubeResponse:
    url = str(payload.url)
    if "youtube.com" not in url and "youtu.be" not in url:
        raise HTTPException(status_code=400, detail="URL must be a YouTube link")

    result = run_youtube_workflow(url)
    status = result.get("status", "failed")
    message = (
        "Video processed successfully"
        if status == "completed"
        else "Video processing failed"
    )
    return YouTubeResponse(
        status=status,
        message=message,
        request_id=result.get("job_id", ""),
        received_url=url,
        summary=result.get("summary") or None,
        error=result.get("error") or None,
    )
