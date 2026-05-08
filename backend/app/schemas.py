from typing import Literal

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    idea: str = Field(..., min_length=3, max_length=300, description="User video idea")
    style: str = Field(..., min_length=2, max_length=50, description="Video style")
    aspect_ratio: Literal["9:16", "16:9", "1:1"] = Field(..., description="Output ratio")


class CreativeBrief(BaseModel):
    theme: str
    target_audience: str
    tone: str
    visual_style: str
    core_selling_point: str


class ScriptOutput(BaseModel):
    title: str
    hook: str
    body: str
    cta: str


class StoryboardShot(BaseModel):
    shot_id: int = Field(..., ge=1)
    duration: int = Field(..., ge=1, le=8)
    scene_description: str
    camera_movement: str
    subtitle: str
    voiceover: str
    image_prompt: str
    preview_image: str | None = None


class ReviewOutput(BaseModel):
    is_valid: bool
    total_duration: int
    suggestions: list[str]


class TimelineItem(BaseModel):
    shot_id: int
    start_second: int
    end_second: int
    subtitle: str


class RenderOutput(BaseModel):
    storyboard_preview: list[StoryboardShot]
    timeline_preview: list[TimelineItem]
    mock_video_preview: dict[str, str]


class GenerateResponse(BaseModel):
    title: str
    brief: CreativeBrief
    script: ScriptOutput
    storyboard: list[StoryboardShot]
    review: ReviewOutput
    timeline: list[TimelineItem]
    render: dict[str, str]
