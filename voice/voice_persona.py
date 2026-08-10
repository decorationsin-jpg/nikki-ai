"""
NIKKI Female Voice Persona & Context-Aware Emotion Controller.
Provides 5 Voice Personas:
1. Warm & Romantic (Default)
2. Soft & Friendly
3. Professional
4. Playful & Energetic
5. Calm & Relaxed

Supports Indian English, Hindi, and Marathi text-to-speech parameter synthesis.
"""

from typing import Dict, Any

class NikkiVoicePersona:
    PERSONAS = {
        "ROMANTIC": {
            "name": "💗 Warm & Romantic",
            "pitch": 1.2,
            "rate": 0.88,
            "volume": 0.95,
            "greetings": ["Good morning, my friend... ❤️", "I'm right here... tell me what you need. ❤️", "Hey... I'm happy to help you."],
            "success": ["Done. That worked perfectly! I'm so happy I could help. ❤️"]
        },
        "FRIENDLY": {
            "name": "🌸 Soft & Friendly",
            "pitch": 1.1,
            "rate": 0.95,
            "volume": 0.9,
            "greetings": ["Hello! I'm Nikki. How can I help you today? 😊", "Hey there! Ready when you are."],
            "success": ["All set! Let me know if you need anything else."]
        },
        "PROFESSIONAL": {
            "name": "💼 Professional",
            "pitch": 1.0,
            "rate": 1.0,
            "volume": 1.0,
            "greetings": ["Nikki system active. How may I assist you?", "Task processor ready."],
            "success": ["Task completed successfully."]
        },
        "PLAYFUL": {
            "name": "✨ Playful",
            "pitch": 1.3,
            "rate": 1.05,
            "volume": 1.0,
            "greetings": ["Yay! I'm ready! What fun thing are we building today? 🚀"],
            "success": ["Boom! Done and dusted! ✨"]
        },
        "CALM": {
            "name": "🌙 Calm & Relaxed",
            "pitch": 0.95,
            "rate": 0.85,
            "volume": 0.85,
            "greetings": ["Take a deep breath... I'm here to take care of everything for you. 🌙"],
            "success": ["Everything is completed smoothly and peacefully."]
        }
    }

    def __init__(self, default_persona: str = "ROMANTIC"):
        self.current_persona = default_persona if default_persona in self.PERSONAS else "ROMANTIC"

    def set_persona(self, persona_key: str) -> str:
        key = persona_key.upper()
        if key in self.PERSONAS:
            self.current_persona = key
            return f"Voice Persona set to: {self.PERSONAS[key]['name']}"
        return f"Unknown persona. Options: {list(self.PERSONAS.keys())}"

    def get_speech_config(self) -> Dict[str, Any]:
        return self.PERSONAS[self.current_persona]

    def format_emotional_response(self, text: str, emotion: str = "normal") -> str:
        cfg = self.PERSONAS[self.current_persona]
        if self.current_persona == "ROMANTIC":
            if emotion == "success":
                return f"Done! {text} ❤️"
            elif emotion == "caring":
                return f"Hey, don't worry... {text} I'm right here with you. ❤️"
            elif emotion == "romantic":
                return f"I'm here... {text} ❤️"
        return text
