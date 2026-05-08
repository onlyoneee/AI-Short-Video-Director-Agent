from __future__ import annotations

from app.llm_client import LLMClient
from app.mock import mock_script
from app.schemas import CreativeBrief, ScriptOutput


class ScriptWriterAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def run(self, brief: CreativeBrief) -> ScriptOutput:
        if self.llm_client.is_mock:
            return ScriptOutput(**mock_script(brief.model_dump()))

        system_prompt = (
            "You are ScriptWriterAgent for short video ads. "
            "Return JSON: title, hook, body, cta."
        )
        user_prompt = (
            "Create an engaging short-video script from this brief:\n"
            f"{brief.model_dump_json(indent=2)}\n"
            "Constraints: dynamic rhythm, strong opening hook, clear call-to-action."
        )
        data = await self.llm_client.chat_json(system_prompt=system_prompt, user_prompt=user_prompt)
        return ScriptOutput(**data)
