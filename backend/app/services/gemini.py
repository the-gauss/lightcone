from __future__ import annotations

from google import genai
from google.genai import types

from backend.app.core.config import settings


_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not settings.google_api_key:
            raise RuntimeError("Missing GOOGLE_AI_STUDIO_API_KEY or GEMINI_API_KEY")
        _client = genai.Client(api_key=settings.google_api_key)
    return _client


def summarize_youtube(
    *,
    url: str,
    title: str,
    description: str,
    media_path: str,
    mime_type: str,
) -> str:
    if not media_path:
        raise RuntimeError("Missing video file for summarization.")

    prompt = (
        "Summarize the YouTube video in 4-6 sentences. "
        "Use the video and audio as the source of truth, avoid generic filler, "
        "and focus on the main topic, key points, and takeaways.\n"
        f"URL: {url}\n"
        f"Title: {title}\n"
        f"Description: {description}\n"
    )

    client = _get_client()
    try:
        uploaded_file = client.files.upload(
            file=media_path,
            config={
                "display_name": f"youtube-{title or 'video'}",
                "mime_type": mime_type or "video/mp4",
            },
        )
    except Exception:
        from backend.app.services.youtube_data import cleanup_media

        cleanup_media(media_path)
        raise
    try:
        if not uploaded_file.uri:
            raise RuntimeError("Failed to upload video to Gemini.")

        import time
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_file = client.files.get(name=uploaded_file.name)

        if uploaded_file.state.name == "FAILED":
             raise RuntimeError(f"Gemini file processing failed: {uploaded_file.error.message}")

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[
                prompt,
                types.Part.from_uri(
                    file_uri=uploaded_file.uri or "",
                    mime_type=uploaded_file.mime_type or mime_type or "video/mp4",
                ),
            ],
        )
    finally:
        try:
            if uploaded_file.name:
                client.files.delete(name=uploaded_file.name)
        except Exception:
            pass
        from backend.app.services.youtube_data import cleanup_media

        cleanup_media(media_path)

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response")
    return text.strip()
