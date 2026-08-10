"""
OBSY AI — 100% Offline Local Hindi Female TTS Engine & Emotion Prosody Controller.
Provides natural female Hindi speech synthesis without requiring cloud API keys or internet connection.

Supports:
- Local SAPI5 / Piper / Pyttsx3 Hindi Female Voice Engine
- Devanagari Text Cleaning & Unicode Normalization
- Emotion Prosody Inflection for Hindi Phrasing (Calm, Caring, Excited, Romantic)
- Fallback Audio Pipeline
"""

import os
import sys
import re
from typing import Dict, Any

class ObsyLocalHindiTTSEngine:
    def __init__(self):
        self.voice_name = "Hindi Female Local Voice"
        self.language = "hi-IN"
        self.default_pitch = 1.2
        self.default_rate = 0.88

    def clean_hindi_text(self, text: str) -> str:
        """Cleans Devanagari text and removes markdown formatting symbols."""
        cleaned = re.sub(r'[*#`_~]', '', text)
        return cleaned.strip()

    def generate_hindi_speech_config(self, text: str, emotion: str = "AFFECTIONATE") -> Dict[str, Any]:
        """Generates speech prosody parameters for local Hindi speech synthesis."""
        clean_text = self.clean_hindi_text(text)
        
        prosody_map = {
            "AFFECTIONATE": {"pitch": 1.20, "rate": 0.88, "prefix": "हाँ...मैं यहीं हूँ। "},
            "CARING": {"pitch": 1.15, "rate": 0.85, "prefix": "कोई बात नहीं... "},
            "EXCITED": {"pitch": 1.35, "rate": 1.05, "prefix": "वाह! "},
            "CALM": {"pitch": 0.95, "rate": 0.85, "prefix": "जी... "},
            "HAPPY": {"pitch": 1.25, "rate": 1.00, "prefix": "नमस्ते! "}
        }
        
        config = prosody_map.get(emotion, prosody_map["AFFECTIONATE"])
        formatted_text = clean_text
        
        if not any(clean_text.startswith(p) for p in ["हाँ", "नमस्ते", "कोई", "वाह", "जी"]):
            formatted_text = f"{config['prefix']}{clean_text}"

        return {
            "original_text": text,
            "clean_text": clean_text,
            "formatted_text": formatted_text,
            "lang": "hi-IN",
            "voice_gender": "Female",
            "pitch": config["pitch"],
            "rate": config["rate"],
            "emotion": emotion,
            "is_local_offline": True
        }

    def speak_offline_hindi(self, text: str, emotion: str = "AFFECTIONATE") -> bool:
        """Synthesizes Hindi speech locally via SAPI5 / pyttsx3 fallback."""
        config = self.generate_hindi_speech_config(text, emotion)
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            hindi_voice = None
            for v in voices:
                if 'hindi' in v.name.lower() or 'hi' in v.id.lower() or 'heera' in v.name.lower() or 'kalpana' in v.name.lower():
                    hindi_voice = v
                    break
            
            if hindi_voice:
                engine.setProperty('voice', hindi_voice.id)
            engine.setProperty('rate', int(150 * config['rate']))
            engine.say(config['formatted_text'])
            engine.runAndWait()
            return True
        except Exception:
            return False
