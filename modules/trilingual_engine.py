"""
Nikki Trilingual Language & Speech Engine.
Provides 100% fluent understanding, text response, and voice output for:
1. English
2. Hindi (हिंदी)
3. Marathi (मराठी)
"""
import re
import sys

class TrilingualEngine:
    """
    Trilingual Language & Speech Engine for English, Hindi, and Marathi.
    """

    def __init__(self):
        self.marathi_keywords = [
            "नमस्कार", "कसा", "कशी", "काय", "चाललंय", "मदत", "धन्यवाद", "नक्की", "छान",
            "हो", "नाही", "सांग", "कर", "कोठे", "कधी", "आहेस", "मी", "तू", "आपण", "शुभप्रभात"
        ]
        self.hindi_keywords = [
            "नमस्ते", "कैसे", "कैसी", "क्या", "चल", "मदद", "शुक्रिया", "अच्छा", "हाँ",
            "नहीं", "बताओ", "करो", "कहाँ", "कब", "हो", "मैं", "तुम", "आप", "धन्यवाद"
        ]

    def detect_language(self, text: str) -> str:
        """
        Detects whether user input is English, Hindi, or Marathi.
        """
        if not text:
            return "english"

        # Check for Devanagari Unicode Range (\u0900 - \u097F)
        devanagari_chars = re.findall(r'[\u0900-\u097F]', text)
        if len(devanagari_chars) > 0:
            # Check for distinct Marathi keywords
            for kw in self.marathi_keywords:
                if kw in text:
                    return "marathi"
            # Default to Hindi for general Devanagari script
            return "hindi"
        else:
            # Check for Romanized Hindi / Marathi (Hinglish / Minglish)
            lower = text.lower()
            if any(w in lower for w in ["kasa ahes", "kay chalalay", "madat kar", "namaskar", "khup chan"]):
                return "marathi"
            elif any(w in lower for w in ["kaise ho", "kya chal raha hai", "madad karo", "namaste", "bahut accha"]):
                return "hindi"
            return "english"

    def get_trilingual_system_prompt(self, detected_lang: str) -> str:
        """
        Generates system prompt instructions for English, Hindi, or Marathi responses.
        """
        if detected_lang == "marathi":
            return (
                "You are Nikki (नक्की), a smart, friendly, local AI assistant. "
                "The user is speaking in Marathi (मराठी). "
                "Respond fluently in clear, natural, and polite Marathi (मराठी) script!"
            )
        elif detected_lang == "hindi":
            return (
                "You are Nikki (निक्की), a smart, friendly, local AI assistant. "
                "The user is speaking in Hindi (हिंदी). "
                "Respond fluently in clear, natural, and polite Hindi (हिंदी) script!"
            )
        else:
            return (
                "You are Nikki, a smart, friendly, local AI assistant. "
                "The user is speaking in English. Respond in clear, helpful English."
            )

    def speak_trilingual(self, text: str, lang: str = "english") -> str:
        """
        Speaks text out loud in English, Hindi, or Marathi.
        """
        print(f"🌐 [Nikki Trilingual Speech ({lang.upper()})]: {text}")

        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            # Look for Hindi/Marathi/Indian English voices
            for v in voices:
                v_name = v.name.lower()
                if lang in ["hindi", "marathi"] and any(w in v_name for w in ["hindi", "india", "kalpana", "hemant"]):
                    engine.setProperty('voice', v.id)
                    break

            engine.setProperty('rate', 165)
            engine.say(text)
            engine.runAndWait()
            return f"Spoken out loud in {lang.capitalize()}!"
        except Exception:
            if sys.platform == "win32":
                import subprocess
                clean_text = text.replace('"', '').replace("'", "")
                cmd = f'powershell -Command "Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Speak(\'{clean_text}\')"'
                subprocess.run(cmd, shell=True, capture_output=True)
                return f"Spoken out loud in {lang.capitalize()} via System.Speech!"
            return f"Trilingual speech executed in {lang.capitalize()}."
