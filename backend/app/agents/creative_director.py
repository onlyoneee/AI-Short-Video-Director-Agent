from __future__ import annotations

from app.llm_client import LLMClient
from app.mock import mock_creative_brief
from app.schemas import CreativeBrief


class CreativeDirectorAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def run(self, idea: str, style: str) -> CreativeBrief:
        if self.llm_client.is_mock:
            return CreativeBrief(**mock_creative_brief(idea=idea, style=style))

        system_prompt = (
            "You are CreativeDirectorAgent for short-form video planning. "
            "Return valid JSON with keys: theme, target_audience, tone, visual_style, core_selling_point."
        )
        user_prompt = (
            f"User idea: {idea}\n"
            f"Video type/style: {style}\n"
            "Analyze and produce a concise creative brief for 15-30 seconds short video."
        )
        data = await self.llm_client.chat_json(system_prompt=system_prompt, user_prompt=user_prompt)
        return CreativeBrief(**data)
