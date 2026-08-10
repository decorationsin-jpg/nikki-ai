"""
Nikki Conversational Learning & Long-Term Memory Engine.
Allows Nikki to learn personal facts, preferences, rules, and memories directly from user conversations,
store them permanently in memory/user_teachings.json, and recall them during future interactions!
"""
import json
import time
from pathlib import Path

class MemoryEngine:
    """
    Long-Term Conversational Memory & Knowledge Persistence Engine.
    """

    def __init__(self, memory_file: str = "memory/user_teachings.json"):
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self._init_store()

    def _init_store(self):
        if not self.memory_file.exists():
            default_mem = {
                "user_facts": {},
                "custom_rules": [],
                "saved_memories": []
            }
            self.memory_file.write_text(json.dumps(default_mem, indent=2), encoding='utf-8')

    def load_teachings(self) -> dict:
        try:
            return json.loads(self.memory_file.read_text(encoding='utf-8'))
        except Exception:
            return {"user_facts": {}, "custom_rules": [], "saved_memories": []}

    def save_teachings(self, data: dict):
        self.memory_file.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def teach_fact(self, key: str, value: str) -> str:
        """Saves a personal fact taught by the user (e.g., 'birthday', 'favorite_color')."""
        mem = self.load_teachings()
        mem.setdefault("user_facts", {})[key.lower()] = value
        self.save_teachings(mem)
        print(f"🧠 [Nikki Memory Engine]: Learned and saved user fact: '{key}' = '{value}'")
        return f"Got it! Nikki has remembered: '{key}' = '{value}'"

    def teach_memory(self, memory_text: str) -> str:
        """Saves a general memory or rule taught by the user."""
        mem = self.load_teachings()
        mem.setdefault("saved_memories", []).append({
            "timestamp": time.ctime(),
            "memory": memory_text
        })
        self.save_teachings(mem)
        print(f"🧠 [Nikki Memory Engine]: Saved new memory: '{memory_text}'")
        return f"Nikki has permanently saved this memory: '{memory_text}'"

    def recall_memories(self, query: str = "") -> str:
        """Recalls relevant memories or facts saved by Nikki."""
        mem = self.load_teachings()
        facts = mem.get("user_facts", {})
        memories = mem.get("saved_memories", [])
        
        report = "🧠 NIKKI RECALLED MEMORIES & TEACHINGS 🧠\n=========================================\n"
        if facts:
            report += "📌 Saved User Facts:\n"
            for k, v in facts.items():
                report += f" - {k.capitalize()}: {v}\n"
        if memories:
            report += "\n📌 Saved Memories & Conversations:\n"
            for item in memories[-5:]:
                report += f" - [{item['timestamp']}] {item['memory']}\n"
        return report if (facts or memories) else "No saved memories found yet."
