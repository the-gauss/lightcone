from __future__ import annotations

from typing import TypedDict

from langgraph.graph import StateGraph


class YouTubeState(TypedDict):
    url: str
    status: str
    job_id: str
    summary: str
    error: str
    video_id: str
    title: str
    description: str
    media_path: str
    mime_type: str


def build_graph():
    graph = StateGraph(YouTubeState)

    def fetch_context(state: YouTubeState) -> YouTubeState:
        from backend.app.services.youtube_data import get_youtube_context

        try:
            context = get_youtube_context(state["url"])
            return {**state, **context}
        except Exception as exc:
            return {
                **state,
                "status": "failed",
                "summary": "",
                "error": str(exc),
                "video_id": "",
                "title": "",
                "description": "",
                "media_path": "",
                "mime_type": "",
            }

    def summarize(state: YouTubeState) -> YouTubeState:
        from backend.app.services.gemini import summarize_youtube

        try:
            if state.get("status") == "failed":
                return state
            summary = summarize_youtube(
                url=state["url"],
                title=state.get("title", ""),
                description=state.get("description", ""),
                media_path=state.get("media_path", ""),
                mime_type=state.get("mime_type", ""),
            )
            return {**state, "status": "completed", "summary": summary, "error": ""}
        except Exception as exc:  # pragma: no cover - last-resort safety net
            return {**state, "status": "failed", "summary": "", "error": str(exc)}

    graph.add_node("fetch_context", fetch_context)
    graph.add_node("summarize", summarize)
    graph.set_entry_point("fetch_context")
    graph.add_edge("fetch_context", "summarize")
    graph.set_finish_point("summarize")
    return graph.compile()
