from __future__ import annotations

from app.llm_client import LLMClient
from app.mock import mock_storyboard
from app.schemas import ScriptOutput, StoryboardShot


class StoryboardAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def run(self, script: ScriptOutput, aspect_ratio: str) -> list[StoryboardShot]:
        if self.llm_client.is_mock:
            return [StoryboardShot(**item) for item in mock_storyboard(script.model_dump(), aspect_ratio)]

        system_prompt = (
            "You are StoryboardAgent. "
            "Split script into 5-8 shots. "
            "Output JSON object with key 'shots' as array of shot objects. "
            "Each shot keys: shot_id, duration, scene_description, camera_movement, subtitle, voiceover, image_prompt."
        )
        user_prompt = (
            f"Script:\n{script.model_dump_json(indent=2)}\n"
            f"Aspect ratio: {aspect_ratio}\n"
            "Constraints: total duration 15-30 sec, varied camera movement, short-video pacing."
        )
        data = await self.llm_client.chat_json(system_prompt=system_prompt, user_prompt=user_prompt)
        shots = data.get("shots", [])
        return [StoryboardShot(**item) for item in shots]
