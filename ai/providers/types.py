from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    id: str | None = None


@dataclass
class LLMResponse:
    text: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    raw_message: Any | None = None