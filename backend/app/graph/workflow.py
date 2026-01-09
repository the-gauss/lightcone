from __future__ import annotations

from typing import TypedDict

from langgraph.graph import StateGraph


class YouTubeState(TypedDict):
    url: str
    status: str
    job_id: str


def build_graph():
    graph = StateGraph(YouTubeState)

    def mark_queued(state: YouTubeState) -> YouTubeState:
        return {**state, "status": "queued"}

    graph.add_node("mark_queued", mark_queued)
    graph.set_entry_point("mark_queued")
    graph.set_finish_point("mark_queued")
    return graph.compile()
