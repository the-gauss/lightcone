from __future__ import annotations

import uuid

from backend.app.graph.workflow import build_graph

_graph = build_graph()


def run_youtube_workflow(url: str) -> dict:
    job_id = str(uuid.uuid4())
    return _graph.invoke(
        {
            "url": url,
            "status": "new",
            "job_id": job_id,
            "summary": "",
            "error": "",
            "video_id": "",
            "title": "",
            "description": "",
            "media_path": "",
            "mime_type": "",
        }
    )
