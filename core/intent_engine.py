"""
NIKKI Response Decision & 25-Intent Analysis Engine.
Analyzes WHAT, WHEN, WHY, HOW, WHO, and REQUIRED ACTIONS from user inputs.

Intent Categories (25 Types):
greeting, farewell, question, explanation, instruction, request, command, reminder, task,
emotional_support, casual_conversation, joke, compliment, gratitude, apology, confirmation,
clarification, disagreement, correction, emergency, privacy, system_control, file_operation,
automation, unknown
"""

import re
from typing import Dict, Any, List, Tuple

class NikkiIntentEngine:
    INTENT_TYPES = [
        "greeting", "farewell", "question", "explanation", "instruction",
        "request", "command", "reminder", "task", "emotional_support",
        "casual_conversation", "joke", "compliment", "gratitude", "apology",
        "confirmation", "clarification", "disagreement", "correction",
        "emergency", "privacy", "system_control", "file_operation",
        "automation", "unknown"
    ]

    @classmethod
    def analyze_intent(cls, user_input: str) -> Dict[str, Any]:
        """Analyzes intent, domain, question type (What/When/Why/How), and confidence."""
        clean_input = user_input.strip()
        lower = clean_input.toLowerCase() if hasattr(clean_input, 'toLowerCase') else clean_input.lower()
        
        intent = "unknown"
        confidence = 0.85
        question_type = "NONE"
        action_required = False
        domain = "GENERAL"
        
        # 1. Question Type Analysis (What/When/Why/How)
        if lower.startswith("what") or "what is" in lower or "what's" in lower:
            question_type = "WHAT"
            intent = "question"
        elif lower.startswith("how") or "how to" in lower or "how do" in lower:
            question_type = "HOW"
            intent = "instruction" if ("do i" in lower or "to" in lower) else "explanation"
        elif lower.startswith("why") or "why is" in lower or "why does" in lower:
            question_type = "WHY"
            intent = "explanation"
            domain = "TROUBLESHOOTING"
        elif lower.startswith("when") or "remind" in lower or "alarm" in lower:
            question_type = "WHEN"
            intent = "reminder"
            action_required = True

        # 2. Greeting & Casual
        if any(w in lower for w in ["hi", "hello", "hey", "good morning", "good evening", "namaste", "namaskar"]):
            intent = "greeting"
            confidence = 0.98

        # 3. Emotional Support
        if any(w in lower for w in ["sad", "difficult day", "feel bad", "crying", "depressed", "help me feel"]):
            intent = "emotional_support"
            confidence = 0.95

        # 4. File Operations & System Control
        if any(w in lower for w in ["create pdf", "open folder", "delete file", "organize files", "run script"]):
            intent = "file_operation"
            action_required = True
            confidence = 0.92

        # 5. Security & Privacy
        if any(w in lower for w in ["privacy", "security", "offline", "data local"]):
            intent = "privacy"
            confidence = 0.98

        return {
            "intent": intent,
            "confidence": confidence,
            "question_type": question_type,
            "action_required": action_required,
            "domain": domain,
            "raw_prompt": clean_input
        }
