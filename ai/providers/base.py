from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a text response from the LLM."""
        pass

    @abstractmethod
    def generate_with_tools(
        self,
        contents: Any,
        tools: Any,
    ) -> Any:
        """
        Generate a response that may contain tool calls.

        The provider receives provider-neutral messages
        and tool definitions.
        """
        pass

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        pass