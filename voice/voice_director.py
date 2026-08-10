"""
OBSY AI Voice Director Subsystem.
Prepares LLM text outputs for AI4Bharat IndicF5 & Indic Parler-TTS neural voice engines.

Responsibilities:
- Emotion Detection & Intensity Mapping
- Prosody Parameter Modulation (Speed, Pitch, Energy)
- Punctuation & Phrase Natural Pause Insertion (..., ,, ।, ?, !)
- Hindi / Hinglish Code-Switching Pronunciation Normalization
"""

import re
from typing import Dict, Any, List

class ObsyVoiceDirector:
    def __init__(self):
        self.emotions = {
            "CARING": {"speed": 0.92, "pitch_shift": -3, "pause_ms": 350, "energy": 0.70},
            "WARM": {"speed": 0.95, "pitch_shift": 0, "pause_ms": 300, "energy": 0.80},
            "ROMANTIC": {"speed": 0.88, "pitch_shift": 2, "pause_ms": 400, "energy": 0.65},
            "EXCITED": {"speed": 1.05, "pitch_shift": 5, "pause_ms": 150, "energy": 0.95},
            "CALM": {"speed": 0.85, "pitch_shift": -5, "pause_ms": 450, "energy": 0.50},
            "EMPATHETIC": {"speed": 0.82, "pitch_shift": -2, "pause_ms": 400, "energy": 0.60}
        }

    def insert_natural_pauses(self, text: str) -> str:
        """Inserts natural prosodic pause markers for IndicF5 audio synthesis."""
        # Replace Devanagari full stop (।) with pause marker
        text = text.replace("।", " । <pause time='300ms'/> ")
        text = text.replace("...", " <pause time='400ms'/> ")
        text = text.replace(",", " , <pause time='200ms'/> ")
        text = text.replace("?", " ? <pause time='350ms'/> ")
        text = text.replace("!", " ! <pause time='250ms'/> ")
        return text

    def direct_speech(self, text: str, emotion_mood: str = "WARM") -> Dict[str, Any]:
        """Prepares complete voice director script payload for IndicF5 / Indic Parler-TTS."""
        clean_text = text.strip()
        phrased_text = self.insert_natural_pauses(clean_text)
        config = self.emotions.get(emotion_mood.upper(), self.emotions["WARM"])

        return {
            "original_text": clean_text,
            "directed_text": phrased_text,
            "emotion": emotion_mood,
            "speed": config["speed"],
            "pitch_shift": config["pitch_shift"],
            "pause_ms": config["pause_ms"],
            "energy": config["energy"],
            "indicf5_ref_clip": f"voice/voices/obsy/hindi/{emotion_mood.lower()}.wav",
            "parler_prompt": f"female speaker, expressive, {emotion_mood.lower()} tone, Indian Hindi accent, clear audio"
        }
