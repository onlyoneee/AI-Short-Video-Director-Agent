from __future__ import annotations

from app.llm_client import LLMClient
from app.mock import mock_render
from app.schemas import RenderOutput, StoryboardShot, TimelineItem


class RenderAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def run(self, storyboard: list[StoryboardShot], aspect_ratio: str) -> RenderOutput:
        data = mock_render([item.model_dump() for item in storyboard], aspect_ratio)
        return RenderOutput(
            storyboard_preview=[StoryboardShot(**item) for item in data["storyboard_preview"]],
            timeline_preview=[TimelineItem(**item) for item in data["timeline_preview"]],
            mock_video_preview=data["mock_video_preview"],
        )
