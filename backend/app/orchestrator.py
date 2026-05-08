from __future__ import annotations

from app.agents import (
    CreativeDirectorAgent,
    RenderAgent,
    ReviewAgent,
    ScriptWriterAgent,
    StoryboardAgent,
    VisualPromptAgent,
)
from app.llm_client import LLMClient
from app.schemas import GenerateRequest, GenerateResponse, StoryboardShot


class AgentOrchestrator:
    def __init__(self) -> None:
        llm_client = LLMClient()
        self.creative_director = CreativeDirectorAgent(llm_client)
        self.script_writer = ScriptWriterAgent(llm_client)
        self.storyboard_agent = StoryboardAgent(llm_client)
        self.visual_prompt_agent = VisualPromptAgent(llm_client)
        self.review_agent = ReviewAgent(llm_client)
        self.render_agent = RenderAgent(llm_client)

    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        brief = await self.creative_director.run(idea=request.idea, style=request.style)
        script = await self.script_writer.run(brief=brief)
        storyboard = await self.storyboard_agent.run(script=script, aspect_ratio=request.aspect_ratio)

        optimized_storyboard: list[StoryboardShot] = []
        for shot in storyboard:
            optimized_prompt = await self.visual_prompt_agent.run(
                image_prompt=shot.image_prompt,
                visual_style=brief.visual_style,
                aspect_ratio=request.aspect_ratio,
            )
            optimized_storyboard.append(
                shot.model_copy(update={"image_prompt": optimized_prompt})
            )

        review = await self.review_agent.run(storyboard=optimized_storyboard)
        render = await self.render_agent.run(
            storyboard=optimized_storyboard,
            aspect_ratio=request.aspect_ratio,
        )

        return GenerateResponse(
            title=script.title,
            brief=brief,
            script=script,
            storyboard=render.storyboard_preview,
            review=review,
            timeline=render.timeline_preview,
            render=render.mock_video_preview,
        )
