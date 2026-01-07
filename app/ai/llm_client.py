from typing import Protocol

class LLMClient(Protocol):
    def chat(self, messages: list[dict[str, str]], *, temperature: float = 0.7): ...