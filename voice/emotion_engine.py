"""
NIKKI Context-Aware Emotion Engine & Speech Prosody System.
Separates 'what NIKKI says' from 'how NIKKI says it'.

Features:
- Dynamic NIKKI_EMOTION State (mood, intensity, empathy, excitement, affection, confidence)
- Context-Driven Sentiment & Emotion Inference
- Prosody Parameter Mapping (Pitch, Rate, Volume, Pauses, Vocal Expressions)
- Non-Verbal Fillers ('Hmm...', 'Oh...', 'Ah...', 'Haha...')
- Temporary Conversation Emotion Timeline Tracker
"""

import re
import time
from typing import Dict, Any, Tuple, List

class NikkiEmotionEngine:
    MOOD_TYPES = ["HAPPY", "CALM", "AFFECTIONATE", "CONCERNED", "EXCITED", "EMPATHETIC", "CURIOUS"]

    def __init__(self):
        self.current_emotion = {
            "mood": "AFFECTIONATE",
            "intensity": 0.65,
            "empathy": 0.80,
            "excitement": 0.25,
            "affection": 0.70,
            "confidence": 0.90
        }
        self.emotion_timeline: List[Dict[str, Any]] = []

    def infer_emotion_from_context(self, user_input: str) -> Dict[str, Any]:
        """Infers NIKKI's emotion state from user prompt context."""
        lower = user_input.lower()
        
        # 1. Happy / Excited Intent
        if any(w in lower for w in ["got the job", "passed", "promoted", "won", "great news", "awesome", "yay", "celebrate"]):
            self.current_emotion.update({
                "mood": "EXCITED",
                "intensity": 0.90,
                "empathy": 0.70,
                "excitement": 0.95,
                "affection": 0.80,
                "confidence": 0.95
            })
        # 2. Empathetic / Concerned Intent
        elif any(w in lower for w in ["difficult day", "sad", "failed", "crying", "lost", "tired", "deleted file", "bad day", "hurt"]):
            self.current_emotion.update({
                "mood": "EMPATHETIC",
                "intensity": 0.75,
                "empathy": 0.95,
                "excitement": 0.10,
                "affection": 0.85,
                "confidence": 0.85
            })
        # 3. Curious Intent
        elif any(w in lower for w in ["what is", "how does", "explain", "tell me about", "why does", "search"]):
            self.current_emotion.update({
                "mood": "CURIOUS",
                "intensity": 0.60,
                "empathy": 0.50,
                "excitement": 0.60,
                "affection": 0.40,
                "confidence": 0.95
            })
        # 4. Affectionate / Warm Intent (Default Companion)
        elif any(w in lower for w in ["love you", "miss you", "nikki", "hi", "hello", "good morning", "thank you", "thanks"]):
            self.current_emotion.update({
                "mood": "AFFECTIONATE",
                "intensity": 0.70,
                "empathy": 0.85,
                "excitement": 0.30,
                "affection": 0.90,
                "confidence": 0.90
            })
        else:
            self.current_emotion.update({
                "mood": "CALM",
                "intensity": 0.50,
                "empathy": 0.60,
                "excitement": 0.20,
                "affection": 0.60,
                "confidence": 0.90
            })

        # Track in Emotion Timeline
        entry = {
            "time": time.strftime("%H:%M"),
            "mood": self.current_emotion["mood"],
            "intensity": self.current_emotion["intensity"],
            "user_prompt": user_input[:40]
        }
        self.emotion_timeline.append(entry)
        if len(self.emotion_timeline) > 20:
            self.emotion_timeline.pop(0)

        return self.current_emotion

    def get_speech_prosody(self, text: str) -> Dict[str, Any]:
        """Calculates exact speech prosody parameters based on current emotion."""
        mood = self.current_emotion["mood"]
        
        prosody_map = {
            "EXCITED": {
                "pitch": 1.35,
                "rate": 1.05,
                "volume": 1.0,
                "pause_ms": 150,
                "filler": "Oh wow! "
            },
            "HAPPY": {
                "pitch": 1.25,
                "rate": 1.0,
                "volume": 1.0,
                "pause_ms": 200,
                "filler": "Haha... "
            },
            "AFFECTIONATE": {
                "pitch": 1.20,
                "rate": 0.88,
                "volume": 0.95,
                "pause_ms": 350,
                "filler": "I'm right here... ❤️ "
            },
            "EMPATHETIC": {
                "pitch": 1.05,
                "rate": 0.82,
                "volume": 0.90,
                "pause_ms": 450,
                "filler": "Oh... take your time. ❤️ "
            },
            "CONCERNED": {
                "pitch": 1.10,
                "rate": 0.85,
                "volume": 0.90,
                "pause_ms": 400,
                "filler": "Oh... don't worry. "
            },
            "CALM": {
                "pitch": 0.95,
                "rate": 0.85,
                "volume": 0.90,
                "pause_ms": 300,
                "filler": "Hmm... "
            },
            "CURIOUS": {
                "pitch": 1.15,
                "rate": 0.98,
                "volume": 0.95,
                "pause_ms": 250,
                "filler": "Let me check... "
            }
        }
        
        config = prosody_map.get(mood, prosody_map["AFFECTIONATE"])
        return {
            "text": text,
            "formatted_text": config["filler"] + text if not text.startswith(("Oh", "Hmm", "Haha", "I'm")) else text,
            "pitch": config["pitch"],
            "rate": config["rate"],
            "volume": config["volume"],
            "pause_ms": config["pause_ms"],
            "mood": mood,
            "emotion_state": self.current_emotion
        }
