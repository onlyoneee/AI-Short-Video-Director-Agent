export type AspectRatio = "9:16" | "16:9" | "1:1";

export interface GenerateRequest {
  idea: string;
  style: string;
  aspect_ratio: AspectRatio;
}

export interface CreativeBrief {
  theme: string;
  target_audience: string;
  tone: string;
  visual_style: string;
  core_selling_point: string;
}

export interface ScriptOutput {
  title: string;
  hook: string;
  body: string;
  cta: string;
}

export interface StoryboardShot {
  shot_id: number;
  duration: number;
  scene_description: string;
  camera_movement: string;
  subtitle: string;
  voiceover: string;
  image_prompt: string;
  preview_image?: string;
}

export interface ReviewOutput {
  is_valid: boolean;
  total_duration: number;
  suggestions: string[];
}

export interface TimelineItem {
  shot_id: number;
  start_second: number;
  end_second: number;
  subtitle: string;
}

export interface GenerateResponse {
  title: string;
  brief: CreativeBrief;
  script: ScriptOutput;
  storyboard: StoryboardShot[];
  review: ReviewOutput;
  timeline: TimelineItem[];
  render: {
    cover_image: string;
    aspect_ratio: string;
    preview_note: string;
  };
}

export type AgentStatus = "pending" | "running" | "success";
