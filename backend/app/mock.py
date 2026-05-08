from __future__ import annotations

import hashlib
from typing import Any


def _seed_text(text: str, max_len: int = 28) -> str:
    compact = " ".join(text.strip().split())
    if len(compact) <= max_len:
        return compact
    return compact[: max_len - 3] + "..."


def mock_creative_brief(idea: str, style: str) -> dict[str, str]:
    base_theme = _seed_text(idea, 40)
    return {
        "theme": f"{base_theme} 的短视频表达",
        "target_audience": "18-35 岁、关注视觉审美和新鲜体验的短视频用户",
        "tone": "未来感、轻快、有冲击力",
        "visual_style": f"{style} + cinematic lighting + clean composition",
        "core_selling_point": "以高辨识度视觉风格快速传达产品记忆点",
    }


def mock_script(brief: dict[str, str]) -> dict[str, str]:
    return {
        "title": "赛博霓虹下的猫咪咖啡时刻",
        "hook": "3 秒抓住注意力：霓虹雨夜中，一杯会发光的猫咪拉花。",
        "body": (
            "镜头跟随一只赛博猫进入未来咖啡馆，展示咖啡制作、香气弥漫、"
            "人与宠物互动场景，强调产品质感和情绪价值。"
        ),
        "cta": "现在就来体验这杯属于未来的温暖，点击了解更多。",
    }


def mock_storyboard(script: dict[str, str], aspect_ratio: str) -> list[dict[str, Any]]:
    shots = [
        {
            "shot_id": 1,
            "duration": 3,
            "scene_description": "雨夜霓虹街道，赛博猫抬头看向发光咖啡馆招牌。",
            "camera_movement": "低机位推进到门口",
            "subtitle": "当夜色亮起，故事从一杯咖啡开始",
            "voiceover": script["hook"],
            "image_prompt": f"cyberpunk neon rainy street, futuristic cat, cafe sign, {aspect_ratio}",
        },
        {
            "shot_id": 2,
            "duration": 4,
            "scene_description": "咖啡师拉花特写，奶泡形成猫咪图案。",
            "camera_movement": "微距横移",
            "subtitle": "一杯会发光的猫咪拉花",
            "voiceover": "细腻奶泡与咖啡香交织，视觉和味觉同步点亮。",
            "image_prompt": f"macro latte art cat shape, chrome cup, soft steam, {aspect_ratio}",
        },
        {
            "shot_id": 3,
            "duration": 3,
            "scene_description": "赛博猫跳上吧台，和顾客互动。",
            "camera_movement": "中景跟拍",
            "subtitle": "每一秒都充满未来感治愈",
            "voiceover": "不仅是咖啡，更是会让你心情升级的陪伴时刻。",
            "image_prompt": f"friendly cyber cat on bar counter, warm neon interior, {aspect_ratio}",
        },
        {
            "shot_id": 4,
            "duration": 4,
            "scene_description": "顾客拿起咖啡走向窗边，城市光影映在杯身。",
            "camera_movement": "环绕镜头 180 度",
            "subtitle": "把城市霓虹，喝进这一口",
            "voiceover": script["body"],
            "image_prompt": f"customer holding glowing coffee by window, bokeh city lights, {aspect_ratio}",
        },
        {
            "shot_id": 5,
            "duration": 4,
            "scene_description": "Logo 与 CTA 出现，猫咪眨眼收尾。",
            "camera_movement": "缓慢拉远",
            "subtitle": "现在就来，体验未来咖啡",
            "voiceover": script["cta"],
            "image_prompt": f"brand logo reveal with cyber cat wink, premium ad frame, {aspect_ratio}",
        },
    ]
    return shots


def mock_review(storyboard: list[dict[str, Any]]) -> dict[str, Any]:
    total_duration = sum(int(item.get("duration", 0)) for item in storyboard)
    suggestions: list[str] = []
    if total_duration < 15:
        suggestions.append("建议增加 1-2 个过渡镜头，提升叙事完整度。")
    if total_duration > 30:
        suggestions.append("建议压缩单镜头时长，提升短视频节奏。")
    if not suggestions:
        suggestions.append("整体节奏良好，可直接用于预览与迭代。")

    return {
        "is_valid": 15 <= total_duration <= 30,
        "total_duration": total_duration,
        "suggestions": suggestions,
    }


def mock_render(storyboard: list[dict[str, Any]], aspect_ratio: str) -> dict[str, Any]:
    timeline = []
    cursor = 0
    storyboard_preview: list[dict[str, Any]] = []
    for shot in storyboard:
        shot_id = int(shot["shot_id"])
        duration = int(shot["duration"])
        preview_url = (
            "https://picsum.photos/seed/"
            + hashlib.md5(f"{shot_id}-{shot['scene_description']}".encode("utf-8")).hexdigest()[:10]
            + "/640/360"
        )
        storyboard_preview.append({**shot, "preview_image": preview_url})
        timeline.append(
            {
                "shot_id": shot_id,
                "start_second": cursor,
                "end_second": cursor + duration,
                "subtitle": shot["subtitle"],
            }
        )
        cursor += duration

    return {
        "storyboard_preview": storyboard_preview,
        "timeline_preview": timeline,
        "mock_video_preview": {
            "cover_image": storyboard_preview[0]["preview_image"] if storyboard_preview else "",
            "aspect_ratio": aspect_ratio,
            "preview_note": "Mock video data only. Replace with real renderer in production.",
        },
    }
