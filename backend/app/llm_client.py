from __future__ import annotations

import json
from typing import Any

import httpx

from app.config import settings


class LLMClientError(Exception):
    """Raised when LLM API invocation fails."""


class LLMClient:
    def __init__(self) -> None:
        self.base_url = settings.LLM_API_BASE_URL.rstrip("/")
        self.api_key = settings.LLM_API_KEY.strip()
        self.model = settings.LLM_MODEL
        self.is_mock = self.api_key == ""

    async def chat_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        if self.is_mock:
            raise LLMClientError("LLM_API_KEY is empty. LLM client is in mock mode.")

        endpoint = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        payload_with_format: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "response_format": {"type": "json_object"},
        }
        payload_fallback: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
        }

        attempts = [payload_with_format, payload_fallback, payload_fallback]
        last_error: Exception | None = None

        async with httpx.AsyncClient(timeout=45) as client:
            for idx, payload in enumerate(attempts, start=1):
                try:
                    response = await client.post(endpoint, headers=headers, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    content = self._extract_content(data)
                    return self._parse_json(content)
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    # First failure may happen if provider does not support response_format.
                    if idx < len(attempts):
                        continue

        raise LLMClientError(f"LLM API call failed after retries: {last_error}") from last_error

    @staticmethod
    def _extract_content(response_json: dict[str, Any]) -> str:
        try:
            return response_json["choices"][0]["message"]["content"]
        except Exception as exc:  # noqa: BLE001
            raise LLMClientError(f"Unexpected response shape: {response_json}") from exc

    @staticmethod
    def _parse_json(content: str) -> dict[str, Any]:
        raw = content.strip()
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.startswith("json"):
                raw = raw[4:].strip()

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMClientError(f"Model output is not valid JSON: {content}") from exc

        if not isinstance(parsed, dict):
            raise LLMClientError("Model output JSON is not an object.")
        return parsed
