import json
import urllib.request
import urllib.error

class LocalLLM:
    """
    Interface for running LLM inference 100% locally using Ollama or LM Studio.
    Requires NO API keys and can run entirely offline.
    """

    def __init__(self, model_name: str = "llama3.2", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host.rstrip('/')

    def is_available(self) -> bool:
        """Checks if local Ollama server is running."""
        try:
            req = urllib.request.Request(f"{self.host}/api/tags")
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except Exception:
            return False

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generates text completion using local Ollama instance.
        """
        if not self.is_available():
            return (
                "[Offline Rule Fallback]: Ollama server is not running at http://localhost:11434.\n"
                "Please run `ollama run llama3.2` in your terminal to start the local LLM brain!"
            )

        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        if system_prompt:
            payload["system"] = system_prompt

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("response", "")
        except urllib.error.URLError as e:
            return f"Error communicating with local LLM: {e}"
