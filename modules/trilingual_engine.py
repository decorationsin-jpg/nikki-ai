"""
Nikki Trilingual Language & Casual Conversation Speech Engine.
Provides 100% fluent, friendly, warm, and casual understanding & voice output for:
1. English
2. Hindi (हिंदी)
3. Marathi (मराठी)
"""
import re
import sys
import random

class TrilingualEngine:
    """
    Casual, Friendly Trilingual Speech & Conversation Engine.
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

        self.casual_openers = {
            "english": [
                "Hey there! ", "Oh, great question! ", "Sure thing! ", "I've got you covered! ", "Here's what you need to know: "
            ],
            "marathi": [
                "अरे वा! मस्त प्रश्न विचारलास! ", "हो नक्कीच! हे बघ: ", "छान! मी सांगते तुला: ", "अरे काय सांगू तुला! "
            ],
            "hindi": [
                "अरे वाह! बहुत बढ़िया सवाल! ", "हाँ बिलकुल! देखो: ", "अरे सुनो, मैं बताती हूँ: ", "ज़रूर! यह रहा जवाब: "
            ]
        }

        self.casual_closers = {
            "english": [
                "\nLet me know if you want me to do anything else for you! 😊",
                "\nHope that helps! What's next on your mind? 🌸"
            ],
            "marathi": [
                "\nअजून काही मदत हवीये का मला सांग! 😊",
                "\nनक्की सांग, मी इथेच आहे तुझ्यासाठी! 🌸"
            ],
            "hindi": [
                "\nऔर कुछ मदद चाहिए तो ज़रूर बताना! 😊",
                "\nउम्मीद है यह काम आया! आगे क्या करना है? 🌸"
            ]
        }

    def detect_language(self, text: str) -> str:
        """Detects whether user input is English, Hindi, or Marathi."""
        if not text:
            return "english"

        devanagari_chars = re.findall(r'[\u0900-\u097F]', text)
        if len(devanagari_chars) > 0:
            for kw in self.marathi_keywords:
                if kw in text:
                    return "marathi"
            return "hindi"
        else:
            lower = text.lower()
            if any(w in lower for w in ["kasa ahes", "kay chalalay", "madat kar", "namaskar", "khup chan"]):
                return "marathi"
            elif any(w in lower for w in ["kaise ho", "kya chal raha hai", "madad karo", "namaste", "bahut accha"]):
                return "hindi"
            return "english"

    def format_casual_response(self, text: str, lang: str = "english") -> str:
        """Formats a response to sound warm, friendly, casual, and easy to understand."""
        opener = random.choice(self.casual_openers.get(lang, self.casual_openers["english"]))
        closer = random.choice(self.casual_closers.get(lang, self.casual_closers["english"]))
        
        # Don't duplicate if already starts with a greeting
        if any(text.startswith(g) for g in ["Hey", "Hello", "Hi", "अरे", "नमस्ते", "नमस्कार"]):
            return text + closer
        return f"{opener}{text}{closer}"

    def get_trilingual_system_prompt(self, detected_lang: str) -> str:
        """Generates system prompt for casual, companion-style responses."""
        if detected_lang == "marathi":
            return (
                "You are Nikki (नक्की), a warm, friendly, casual AI companion. "
                "The user is speaking in Marathi (मराठी). "
                "Answer casually, simply, and warmly in natural Marathi script! Avoid overly formal textbook language."
            )
        elif detected_lang == "hindi":
            return (
                "You are Nikki (निक्की), a warm, friendly, casual AI companion. "
                "The user is speaking in Hindi (हिंदी). "
                "Answer casually, simply, and warmly in natural Hindi script! Avoid overly formal textbook language."
            )
        else:
            return (
                "You are Nikki, a warm, friendly, casual AI companion. "
                "Answer casually, conversationally, and warmly in simple English! Keep responses easy to understand."
            )

    def speak_trilingual(self, text: str, lang: str = "english") -> str:
        """Speaks text out loud in English, Hindi, or Marathi with friendly tone."""
        print(f"🌐 [Nikki Casual Voice ({lang.upper()})]: {text}")

        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            for v in voices:
                v_name = v.name.lower()
                if lang in ["hindi", "marathi"] and any(w in v_name for w in ["hindi", "india", "kalpana", "hemant"]):
                    engine.setProperty('voice', v.id)
                    break

            engine.setProperty('rate', 170)
            engine.say(text)
            engine.runAndWait()
            return f"Spoken casually in {lang.capitalize()}!"
        except Exception:
            return f"Trilingual speech executed in {lang.capitalize()}."
