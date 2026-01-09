from __future__ import annotations

import uuid

from backend.app.graph.workflow import build_graph

_graph = build_graph()


def enqueue_youtube_processing(url: str) -> str:
    job_id = str(uuid.uuid4())
    _graph.invoke({"url": url, "status": "new", "job_id": job_id})
    return job_id
