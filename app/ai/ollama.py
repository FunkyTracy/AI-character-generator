import requests

class OllamaLLM:
    def __init__(self, model: str="qwen2.5", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url= base_url.rstrip("/")

    def chat(self, messages: list[dict[str, str]], *, temperature: float = 0.7) -> str:
        r = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature},
            },
            timeout=120,
        )

        r.raise_for_status()
        data = r.json()
        
        return data["message"]["content"]