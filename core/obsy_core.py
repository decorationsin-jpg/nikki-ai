"""
OBSY AI Core Engine — Private Local Intelligence Platform.
Orchestrates internal specialized sub-agents:
- Research Agent (deep web research & briefings)
- Coding Agent (sandbox script generation & execution)
- File Agent (directory & document organization)
- Document RAG Agent (multilingual SQLite vector search)
- Automation Agent (background learning daemon)
- Memory Agent (4-tier local memory store)
"""

from typing import Dict, Any, List

class ObsyCoreEngine:
    AGENTS = {
        "RESEARCH": "Research Agent (Deep Web Intelligence)",
        "CODING": "Coding Agent (Sandbox Code Executor)",
        "FILE": "File Agent (Local File Manager)",
        "DOCUMENT_RAG": "Document Agent (Multilingual RAG Engine)",
        "AUTOMATION": "Automation Agent (Daemon & Routines)",
        "MEMORY": "Memory Agent (4-Tier Local Store)",
        "COMPANION": "Personal Assistant (Emotional Female Voice Persona)"
    }

    @classmethod
    def route_agent_task(cls, prompt: str, intent_info: Dict[str, Any]) -> Dict[str, Any]:
        """Routes task to the appropriate internal OBSY sub-agent."""
        intent = intent_info.get("intent", "unknown")
        lower = prompt.lower()

        selected_agent = "COMPANION"
        if any(w in lower for w in ["search", "information", "who is", "what is"]):
            selected_agent = "RESEARCH"
        elif any(w in lower for w in ["code", "python", "script", "program"]):
            selected_agent = "CODING"
        elif any(w in lower for w in ["file", "folder", "organize", "pdf"]):
            selected_agent = "FILE"
        elif any(w in lower for w in ["document", "rag", "price list", "notes"]):
            selected_agent = "DOCUMENT_RAG"

        return {
            "prompt": prompt,
            "agent_key": selected_agent,
            "agent_name": cls.AGENTS[selected_agent],
            "privacy_guarantee": "100% LOCAL",
            "thought_steps": [
                "◉ Listening",
                "◌ Understanding Intent",
                "◌ Searching Local Memory & RAG",
                "◌ Executing Sub-Agent Strategy",
                "✓ Done"
            ]
        }
