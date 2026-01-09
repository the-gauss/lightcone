from __future__ import annotations

import mimetypes
import re
import tempfile
from pathlib import Path
from typing import Any

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from backend.app.core.config import settings

_VIDEO_ID_PATTERNS = [
    re.compile(r"youtu\.be/(?P<id>[^?&#/]+)"),
    re.compile(r"youtube\.com/watch\?v=(?P<id>[^?&#/]+)"),
    re.compile(r"youtube\.com/embed/(?P<id>[^?&#/]+)"),
    re.compile(r"youtube\.com/shorts/(?P<id>[^?&#/]+)"),
]


def extract_video_id(url: str) -> str | None:
    for pattern in _VIDEO_ID_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group("id")
    return None


def download_video(url: str) -> tuple[Path, dict[str, Any]]:
    max_bytes = settings.max_video_mb * 1024 * 1024
    temp_dir = Path(tempfile.mkdtemp(prefix="lightcone-video-"))
    output_template = str(temp_dir / "%(id)s.%(ext)s")
    ydl_opts = {
        "format": "worst[ext=mp4][acodec!=none][vcodec!=none]",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "max_filesize": max_bytes,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = None
            requested = info.get("requested_downloads") or []
            if requested:
                filepath = requested[0].get("filepath")
            if not filepath:
                filepath = ydl.prepare_filename(info)
    except DownloadError as exc:
        message = str(exc)
        if "max-filesize" in message.lower() or "filesize" in message.lower():
            raise RuntimeError(
                f"Video exceeds MAX_VIDEO_MB ({settings.max_video_mb} MB)."
            ) from exc
        if "ffmpeg" in message.lower():
            raise RuntimeError(
                "Video download requires ffmpeg to merge streams. Install ffmpeg or try another video."
            ) from exc
        raise RuntimeError("Failed to download video for summarization.") from exc

    path = Path(filepath)
    if not path.exists():
        raise RuntimeError("Video download failed.")
    return path, info


def cleanup_media(path: str) -> None:
    file_path = Path(path)
    if file_path.exists():
        file_path.unlink()
    parent = file_path.parent
    if parent.exists():
        try:
            parent.rmdir()
        except OSError:
            return


def get_youtube_context(url: str) -> dict[str, Any]:
    video_id = extract_video_id(url) or ""
    media_path, info = download_video(url)
    if not video_id:
        video_id = info.get("id") or ""
    if not video_id:
        raise ValueError("Could not extract a YouTube video id")
    mime_type, _ = mimetypes.guess_type(media_path)
    if not mime_type:
        mime_type = f"video/{media_path.suffix.lstrip('.') or 'mp4'}"

    title = info.get("title") or ""
    description = info.get("description") or ""
    return {
        "video_id": video_id,
        "title": title,
        "description": description,
        "media_path": str(media_path),
        "mime_type": mime_type,
    }
