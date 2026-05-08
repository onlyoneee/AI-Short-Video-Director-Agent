import { useMemo, useState } from "react";
import { generateStoryboard } from "./api";
import type { AgentStatus, GenerateResponse } from "./types";

const STYLE_OPTIONS = [
  "商业广告",
  "剧情短片",
  "小红书种草",
  "科技产品宣传",
  "知识科普",
] as const;

const RATIO_OPTIONS = ["9:16", "16:9", "1:1"] as const;

const AGENTS = [
  "CreativeDirectorAgent",
  "ScriptWriterAgent",
  "StoryboardAgent",
  "VisualPromptAgent",
  "ReviewAgent",
  "RenderAgent",
] as const;

type AgentName = (typeof AGENTS)[number];
type AgentStateMap = Record<AgentName, AgentStatus>;

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

function initAgentStates(): AgentStateMap {
  return AGENTS.reduce(
    (acc, item) => ({ ...acc, [item]: "pending" }),
    {} as AgentStateMap
  );
}

export default function App() {
  const [idea, setIdea] = useState("帮我生成一个未来感咖啡广告");
  const [style, setStyle] = useState<(typeof STYLE_OPTIONS)[number]>("商业广告");
  const [aspectRatio, setAspectRatio] = useState<(typeof RATIO_OPTIONS)[number]>("9:16");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [agentStates, setAgentStates] = useState<AgentStateMap>(initAgentStates());

  const canGenerate = useMemo(() => idea.trim().length >= 3 && !loading, [idea, loading]);

  async function animateWorkflow() {
    for (const agent of AGENTS) {
      setAgentStates((prev) => ({ ...prev, [agent]: "running" }));
      await sleep(350);
      setAgentStates((prev) => ({ ...prev, [agent]: "success" }));
      await sleep(220);
    }
  }

  async function onGenerate() {
    if (!canGenerate) return;
    setLoading(true);
    setError("");
    setResult(null);
    setAgentStates(initAgentStates());

    try {
      const workflowTask = animateWorkflow();
      const response = await generateStoryboard({
        idea: idea.trim(),
        style,
        aspect_ratio: aspectRatio,
      });
      await workflowTask;
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "生成失败，请稍后再试。");
    } finally {
      setLoading(false);
    }
  }

  function onExportJson() {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: "application/json;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "storyboard-result.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="min-h-screen px-4 py-8 text-slate-100 md:px-8">
      <main className="mx-auto max-w-6xl space-y-6">
        <section className="rounded-2xl border border-border bg-panel/90 p-6 shadow-card">
          <h1 className="text-2xl font-bold tracking-wide md:text-3xl">
            AI Short Video Director Agent
          </h1>
          <p className="mt-2 text-slate-300">
            输入一句创意，多个 AI Agent 自动生成短视频 storyboard。
          </p>
        </section>

        <section className="grid gap-4 rounded-2xl border border-border bg-panel/80 p-6 shadow-card md:grid-cols-3">
          <label className="md:col-span-3">
            <div className="mb-2 text-sm text-slate-300">视频创意</div>
            <textarea
              className="h-24 w-full rounded-xl border border-border bg-slate-900/70 p-3 outline-none transition focus:border-accent"
              placeholder="例如：帮我生成一个未来感咖啡广告"
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
            />
          </label>

          <label>
            <div className="mb-2 text-sm text-slate-300">视频类型</div>
            <select
              value={style}
              onChange={(e) => setStyle(e.target.value as (typeof STYLE_OPTIONS)[number])}
              className="w-full rounded-xl border border-border bg-slate-900/70 p-3 outline-none focus:border-accent"
            >
              {STYLE_OPTIONS.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>

          <label>
            <div className="mb-2 text-sm text-slate-300">视频比例</div>
            <select
              value={aspectRatio}
              onChange={(e) => setAspectRatio(e.target.value as (typeof RATIO_OPTIONS)[number])}
              className="w-full rounded-xl border border-border bg-slate-900/70 p-3 outline-none focus:border-accent"
            >
              {RATIO_OPTIONS.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>

          <div className="flex items-end">
            <button
              className="w-full rounded-xl bg-accent px-4 py-3 font-semibold text-slate-950 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={!canGenerate}
              onClick={onGenerate}
            >
              {loading ? "Generating..." : "Generate"}
            </button>
          </div>
          {error ? <p className="md:col-span-3 text-sm text-red-300">{error}</p> : null}
        </section>

        <section className="rounded-2xl border border-border bg-panel/80 p-6 shadow-card">
          <h2 className="text-lg font-semibold">Multi-Agent Workflow</h2>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            {AGENTS.map((agent) => {
              const status = agentStates[agent];
              return (
                <div
                  key={agent}
                  className="rounded-xl border border-border bg-slate-900/50 p-3 text-sm"
                >
                  <div className="font-medium">{agent}</div>
                  <div className="mt-1 text-xs text-slate-300">
                    Status:{" "}
                    <span
                      className={
                        status === "success"
                          ? "text-success"
                          : status === "running"
                            ? "text-pending"
                            : "text-slate-400"
                      }
                    >
                      {status}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {result ? (
          <>
            <section className="rounded-2xl border border-border bg-panel/80 p-6 shadow-card">
              <h3 className="text-lg font-semibold">1. 视频标题</h3>
              <p className="mt-3 text-xl">{result.title}</p>
            </section>

            <section className="rounded-2xl border border-border bg-panel/80 p-6 shadow-card">
              <h3 className="text-lg font-semibold">2. Creative Brief</h3>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <CardItem label="Theme" value={result.brief.theme} />
                <CardItem label="Target Audience" value={result.brief.target_audience} />
                <CardItem label="Tone" value={result.brief.tone} />
                <CardItem label="Visual Style" value={result.brief.visual_style} />
                <CardItem label="Core Selling Point" value={result.brief.core_selling_point} />
              </div>
            </section>

            <section className="rounded-2xl border border-border bg-panel/80 p-6 shadow-card">
              <h3 className="text-lg font-semibold">3. 视频脚本</h3>
              <div className="mt-4 space-y-2 text-slate-200">
                <p>
                  <span className="text-slate-400">Hook：</span>
                  {result.script.hook}
                </p>
                <p>
                  <span className="text-slate-400">Body：</span>
                  {result.script.body}
                </p>
                <p>
                  <span className="text-slate-400">CTA：</span>
                  {result.script.cta}
                </p>
              </div>
            </section>

            <section className="rounded-2xl border border-border bg-panel/80 p-6 shadow-card">
              <h3 className="text-lg font-semibold">4. Storyboard</h3>
              <div className="mt-4 grid gap-4 md:grid-cols-2">
                {result.storyboard.map((shot) => (
                  <article
                    key={shot.shot_id}
                    className="rounded-xl border border-border bg-slate-900/60 p-4"
                  >
                    <img
                      src={shot.preview_image || "https://picsum.photos/640/360"}
                      alt={`shot-${shot.shot_id}`}
                      className="h-44 w-full rounded-lg object-cover"
                    />
                    <div className="mt-3 text-sm">
                      <p>
                        <span className="text-slate-400">镜头：</span>#{shot.shot_id}
                      </p>
                      <p>
                        <span className="text-slate-400">时长：</span>
                        {shot.duration}s
                      </p>
                      <p>
                        <span className="text-slate-400">Scene：</span>
                        {shot.scene_description}
                      </p>
                      <p>
                        <span className="text-slate-400">Camera：</span>
                        {shot.camera_movement}
                      </p>
                      <p>
                        <span className="text-slate-400">Subtitle：</span>
                        {shot.subtitle}
                      </p>
                      <p>
                        <span className="text-slate-400">Voiceover：</span>
                        {shot.voiceover}
                      </p>
                      <p className="mt-2 rounded-md bg-slate-800/80 p-2 text-xs text-slate-300">
                        <span className="text-slate-400">Image Prompt：</span>
                        {shot.image_prompt}
                      </p>
                    </div>
                  </article>
                ))}
              </div>
            </section>

            <section className="rounded-2xl border border-border bg-panel/80 p-6 shadow-card">
              <h3 className="text-lg font-semibold">Timeline</h3>
              <div className="mt-4 space-y-3">
                {result.timeline.map((item) => (
                  <div key={item.shot_id} className="rounded-lg border border-border bg-slate-900/50 p-3">
                    <p className="text-sm">
                      Shot #{item.shot_id} | {item.start_second}s - {item.end_second}s
                    </p>
                    <p className="mt-1 text-xs text-slate-300">{item.subtitle}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="flex flex-wrap gap-3 pb-10">
              <button
                className="rounded-xl border border-accent px-4 py-2 text-accent transition hover:bg-accent hover:text-slate-950"
                onClick={onGenerate}
                disabled={loading}
              >
                Regenerate
              </button>
              <button
                className="rounded-xl border border-border px-4 py-2 transition hover:border-accent"
                onClick={onExportJson}
              >
                Export JSON
              </button>
            </section>
          </>
        ) : null}
      </main>
    </div>
  );
}

function CardItem(props: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-border bg-slate-900/60 p-3">
      <p className="text-xs text-slate-400">{props.label}</p>
      <p className="mt-1 text-sm">{props.value}</p>
    </div>
  );
}
