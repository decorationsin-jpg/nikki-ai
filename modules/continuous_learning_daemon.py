"""
24/7 Continuous Learning & Autonomous Background Memory Daemon for Nikki.
Runs continuously in the background to scrape web knowledge, update long-term memory,
refine custom skills, and index user topics without stopping!
"""
import time
import json
import threading
from pathlib import Path
from modules.web_search import FreeWebSearch
from modules.self_modifier import SelfModifier

class ContinuousLearningDaemon:
    """
    24/7 Background Engine for continuous learning and memory expansion.
    """

    def __init__(self, memory_dir: str = "memory", sleep_interval_sec: int = 3600):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.sleep_interval_sec = sleep_interval_sec
        self.is_running = False
        self.web = FreeWebSearch()
        self.modifier = SelfModifier()
        
        self.memory_file = self.memory_dir / "long_term_memory.json"
        self.knowledge_file = self.memory_dir / "knowledge_base.json"
        self._init_memory()

    def _init_memory(self):
        """Initializes long-term memory files if they don't exist."""
        if not self.memory_file.exists():
            default_mem = {
                "assistant_name": "Nikki",
                "creation_time": time.ctime(),
                "learned_topics": [],
                "user_preferences": {},
                "total_background_cycles": 0
            }
            self.memory_file.write_text(json.dumps(default_mem, indent=2), encoding='utf-8')

        if not self.knowledge_file.exists():
            self.knowledge_file.write_text(json.dumps([], indent=2), encoding='utf-8')

    def load_memory(self) -> dict:
        """Reads long-term memory data."""
        try:
            return json.loads(self.memory_file.read_text(encoding='utf-8'))
        except Exception:
            return {}

    def save_memory(self, memory_data: dict):
        """Persists updated memory data to disk."""
        self.memory_file.write_text(json.dumps(memory_data, indent=2), encoding='utf-8')

    def add_knowledge_item(self, topic: str, content: str):
        """Stores new knowledge into the 24/7 knowledge base."""
        try:
            kb = json.loads(self.knowledge_file.read_text(encoding='utf-8'))
        except Exception:
            kb = []

        kb.append({
            "timestamp": time.ctime(),
            "topic": topic,
            "content": content[:1000]
        })
        self.knowledge_file.write_text(json.dumps(kb, indent=2), encoding='utf-8')
        print(f"🧠 [Nikki 24/7 Learning]: Added new knowledge item for topic: '{topic}'")

    def run_learning_cycle(self):
        """Single learning cycle executed by the background daemon."""
        print(f"\n🌙 [Nikki 24/7 Daemon]: Running background learning cycle ({time.ctime()})...")
        mem = self.load_memory()
        mem["total_background_cycles"] = mem.get("total_background_cycles", 0) + 1

        # 1. Learn new topic via free web search
        sample_topics = ["Python programming tips", "AI technology trends", "System automation tools"]
        target_topic = sample_topics[mem["total_background_cycles"] % len(sample_topics)]

        print(f"🌐 [Nikki 24/7 Learning]: Scraping knowledge for '{target_topic}'...")
        results = self.web.search(target_topic, max_results=3)

        if results:
            self.add_knowledge_item(target_topic, str(results))
            if target_topic not in mem.get("learned_topics", []):
                mem.setdefault("learned_topics", []).append(target_topic)

        self.save_memory(mem)
        print(f"✅ [Nikki 24/7 Daemon]: Cycle #{mem['total_background_cycles']} completed.")

    def start_daemon_in_background(self):
        """Launches the 24/7 continuous learning loop in a separate background thread."""
        if self.is_running:
            return "24/7 Learning Daemon is already running!"

        self.is_running = True

        def daemon_loop():
            while self.is_running:
                try:
                    self.run_learning_cycle()
                except Exception as e:
                    print(f"Error in 24/7 daemon cycle: {str(e)}")
                time.sleep(self.sleep_interval_sec)

        thread = threading.Thread(target=daemon_loop, daemon=True)
        thread.start()
        return "🚀 Nikki's 24/7 Continuous Learning Daemon has been launched in the background!"

    def stop_daemon(self):
        """Stops the 24/7 background learning loop."""
        self.is_running = False
        return "Stopped 24/7 Continuous Learning Daemon."
