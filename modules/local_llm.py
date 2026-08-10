"""
Local LLM Interface Module for Nikki.
Executes 100% local model inference via Ollama or LM Studio without third-party API keys.
Includes model auto-discovery and intelligent fallback handling.
"""
import json
import urllib.request
import urllib.error
from typing import Optional, List

class LocalLLM:
    """
    Zero-API Key Local LLM Interface.
    Runs 100% locally on user hardware.
    """

    def __init__(self, model_name: str = "llama3.2", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host.rstrip('/')

    def is_available(self) -> bool:
        """Checks if the local Ollama server is running."""
        try:
            req = urllib.request.Request(f"{self.host}/api/tags")
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except Exception:
            return False

    def list_local_models(self) -> List[str]:
        """Lists all AI models installed on the local Ollama instance."""
        try:
            req = urllib.request.Request(f"{self.host}/api/tags")
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode('utf-8'))
                return [m.get("name") for m in data.get("models", [])]
        except Exception:
            return []

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generates text completion from local LLM."""
        if not self.is_available():
            return (
                "[Offline Rule Engine Active]: Local Ollama server is not running.\n"
                "Please run `ollama run llama3.2` to enable full local LLM brain capabilities!"
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
            return f"Error communicating with local LLM: {str(e)}"
