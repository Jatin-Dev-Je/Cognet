"""OpenAI client shim for Cognet.

Purpose:
Provide a minimal client interface for summarization and future API integration.
"""

from __future__ import annotations


class _Message:
	def __init__(self, content: str) -> None:
		self.content = content


class _Choice:
	def __init__(self, content: str) -> None:
		self.message = _Message(content)


class _CompletionResponse:
	def __init__(self, content: str) -> None:
		self.choices = [_Choice(content)]


class _ChatCompletions:
	def create(self, model: str, messages: list[dict[str, str]]) -> _CompletionResponse:
		prompt = messages[-1]["content"] if messages else ""
		lines = [line.strip("-• \t") for line in prompt.splitlines() if line.strip()]
		activity_lines = [line for line in lines if not line.lower().startswith("summarize") and not line.lower().startswith("keep it")]
		compressed = "\n".join(f"- {line}" for line in activity_lines[:5]) or "- No meaningful activity found."
		return _CompletionResponse(compressed)


class _Chat:
	def __init__(self) -> None:
		self.completions = _ChatCompletions()


class _Client:
	def __init__(self) -> None:
		self.chat = _Chat()


client = _Client()
