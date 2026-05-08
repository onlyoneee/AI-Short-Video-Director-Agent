from __future__ import annotations

from app.llm_client import LLMClient
from app.mock import mock_review
from app.schemas import ReviewOutput, StoryboardShot


class ReviewAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def run(self, storyboard: list[StoryboardShot]) -> ReviewOutput:
        if self.llm_client.is_mock:
            return ReviewOutput(**mock_review([item.model_dump() for item in storyboard]))

        system_prompt = (
            "You are ReviewAgent for short videos. "
            "Check coherence, pacing, total duration, subtitle naturalness, style consistency. "
            "Return JSON: is_valid(boolean), total_duration(number), suggestions(array of strings)."
        )
        user_prompt = (
            "Review this storyboard:\n"
            + "\n".join(item.model_dump_json() for item in storyboard)
        )
        data = await self.llm_client.chat_json(system_prompt=system_prompt, user_prompt=user_prompt)
        return ReviewOutput(**data)
