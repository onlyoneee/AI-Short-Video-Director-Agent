from __future__ import annotations

from app.llm_client import LLMClient


class VisualPromptAgent:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def run(self, image_prompt: str, visual_style: str, aspect_ratio: str) -> str:
        if self.llm_client.is_mock:
            return (
                f"{image_prompt}, cinematic composition, dramatic rim light, "
                f"volumetric fog, rich texture details, lens language, unified {visual_style}, {aspect_ratio}"
            )

        system_prompt = (
            "You are VisualPromptAgent. Optimize image prompt for cinematic consistency. "
            "Return JSON with key: optimized_prompt."
        )
        user_prompt = (
            f"Original prompt: {image_prompt}\n"
            f"Target visual style: {visual_style}\n"
            f"Aspect ratio: {aspect_ratio}\n"
            "Add camera language, composition, lighting, material, and style coherence."
        )
        data = await self.llm_client.chat_json(system_prompt=system_prompt, user_prompt=user_prompt)
        return str(data["optimized_prompt"])
