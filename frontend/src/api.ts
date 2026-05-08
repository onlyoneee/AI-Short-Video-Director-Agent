import type { GenerateRequest, GenerateResponse } from "./types";

const API_BASE = "http://localhost:8000";

export async function generateStoryboard(
  payload: GenerateRequest
): Promise<GenerateResponse> {
  const response = await fetch(`${API_BASE}/api/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Generate request failed.");
  }

  return (await response.json()) as GenerateResponse;
}
