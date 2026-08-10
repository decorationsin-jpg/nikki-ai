"""
NIKKI 11-Language Multilingual Architecture & Code-Switching Engine.
Supports 11 Primary Languages:
1. English (en-IN)
2. Hindi (hi-IN / हिंदी)
3. Marathi (mr-IN / मराठी)
4. Bengali (bn-IN / বাংলা)
5. Gujarati (gu-IN / ગુજરાતી)
6. Tamil (ta-IN / தமிழ்)
7. Telugu (te-IN / తెలుగు)
8. Kannada (kn-IN / ಕನ್ನಡ)
9. Malayalam (ml-IN / മലയാളം)
10. Punjabi (pa-IN / ਪੰਜਾਬੀ)
11. Urdu (ur-IN / اردو)

Features:
- Character & Script Language Detection (Devanagari, Bengali, Tamil, etc.)
- Code-Switching Processor (Hinglish, Minglish, mixed language phrases)
- Language-Neutral Intent Representation
- Multilingual Romantic Female Persona Phrasing
"""

import re
from typing import Dict, Any, Tuple

class NikkiMultilingualEngine:
    LANGUAGES = {
        "en": {"name": "English", "locale": "en-IN", "script": "Latin"},
        "hi": {"name": "Hindi (हिंदी)", "locale": "hi-IN", "script": "Devanagari"},
        "mr": {"name": "Marathi (मराठी)", "locale": "mr-IN", "script": "Devanagari"},
        "bn": {"name": "Bengali (বাংলা)", "locale": "bn-IN", "script": "Bengali"},
        "gu": {"name": "Gujarati (ગુજરાતી)", "locale": "gu-IN", "script": "Gujarati"},
        "ta": {"name": "Tamil (தமிழ்)", "locale": "ta-IN", "script": "Tamil"},
        "te": {"name": "Telugu (తెలుగు)", "locale": "te-IN", "script": "Telugu"},
        "kn": {"name": "Kannada (ಕನ್ನಡ)", "locale": "kn-IN", "script": "Kannada"},
        "ml": {"name": "Malayalam (മലയാളം)", "locale": "ml-IN", "script": "Malayalam"},
        "pa": {"name": "Punjabi (ਪੰਜਾਬੀ)", "locale": "pa-IN", "script": "Gurmukhi"},
        "ur": {"name": "Urdu (اردو)", "locale": "ur-IN", "script": "Arabic"}
    }

    ROMANTIC_PHRASES = {
        "en": {
            "greeting": "Good morning... ❤️ I'm NIKKI. What would you like to do today?",
            "here_for_you": "Of course, I'm here for you. ❤️",
            "working_on_it": "Sure! Let me take care of that for you. ❤️",
            "success": "Done! That worked perfectly. I'm happy I could help. ❤️"
        },
        "hi": {
            "greeting": "नमस्ते... ❤️ मैं निक्की हूँ। आज मैं आपकी क्या मदद कर सकती हूँ?",
            "here_for_you": "बिल्कुल… मैं यहीं हूँ आपके लिए। ❤️",
            "working_on_it": "जी बिल्कुल, मैं आपके लिए यह कर देती हूँ। ❤️",
            "success": "हो गया! यह काम एकदम सही हुआ। ❤️"
        },
        "mr": {
            "greeting": "शुभ प्रभात... ❤️ मी नक्की आहे. आज आपण काय करूया?",
            "here_for_you": "नक्की… मी तुझ्यासाठी इथेच आहे. ❤️",
            "working_on_it": "हो नक्की, मी तुझ्यासाठी हे करून देते. ❤️",
            "success": "झालं! हे काम पूर्ण झालं आहे. ❤️"
        },
        "bn": {
            "greeting": "শুভ সকাল... ❤️ আমি নিক্কি। আজ আপনাকে কীভাবে সাহায্য করতে পারি?",
            "here_for_you": "অবশ্যই… আমি তোমার জন্য আছি। ❤️",
            "working_on_it": "অবশ্যই, আমি আপনার জন্য এটি করে দিচ্ছি। ❤️",
            "success": "হয়ে গেছে! কাজটা একদম নিখুঁত হয়েছে। ❤️"
        },
        "gu": {
            "greeting": "સુપ્રભાત... ❤️ હું નિક્કી છું. આજે હું તમારી શું મદદ કરી શકું?",
            "here_for_you": "ચોક્કસ… હું તમારા માટે અહીં જ છું. ❤️",
            "working_on_it": "હા ચોક્કસ, હું તમારા માટે આ કરી દઉં છું. ❤️",
            "success": "થઈ ગયું! આ કામ એકદમ યોગ્ય રીતે થયું. ❤️"
        },
        "ta": {
            "greeting": "காலை வணக்கம்... ❤️ நான் நிக்கி. இன்று உங்களுக்கு எவ்வாறு உதவட்டும்?",
            "here_for_you": "நிச்சயமாக… நான் உங்களுக்காக இங்கே இருக்கிறேன். ❤️",
            "working_on_it": "நிச்சயமாக, நான் உங்களுக்காக இதைச் செய்கிறேன். ❤️",
            "success": "முடிந்தது! இது மிகச்சரியாக முடிந்தது. ❤️"
        },
        "te": {
            "greeting": "శుభోదయం... ❤️ నేను నిక్కి. ఈరోజు మీకు ఎలా సహాయపడను?",
            "here_for_you": "తప్పకుండా… నేను మీ కోసం ఇక్కడే ఉన్నాను. ❤️",
            "working_on_it": "ఖచ్చితంగా, నేను మీ కోసం ఇది చేస్తాను. ❤️",
            "success": "పూర్తయింది! ఇది చాలా చక్కగా జరిగింది. ❤️"
        },
        "kn": {
            "greeting": "ಶುಭೋದಯ... ❤️ ನಾನು ನಿಕ್ಕಿ. ಇಂದು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ?",
            "here_for_you": "ಖಂಡಿತ... ನಾನು ನಿಮಗಾಗಿ ಇಲ್ಲಿದ್ದೇನೆ. ❤️",
            "working_on_it": "ಖಂಡಿತ, ನಾನು ನಿಮಗಾಗಿ ಇದನ್ನು ಮಾಡುತ್ತೇನೆ. ❤️",
            "success": "ಆಯಿತು! ಇದು ಯಶಸ್ವಿಯಾಗಿ ಪೂರ್ಣಗೊಂಡಿದೆ. ❤️"
        },
        "ml": {
            "greeting": "സുപ്രഭാതം... ❤️ ഞാൻ നിക്കി. ഇന്ന് ഞാൻ നിങ്ങളെ എങ്ങനെ സഹായിക്കണം?",
            "here_for_you": "തീർച്ചയായും... ഞാൻ നിങ്ങൾക്കായി ഇവിടെയുണ്ട്. ❤️",
            "working_on_it": "തീർച്ചയായും, ഞാൻ നിങ്ങൾക്കായി ഇത് ചെയ്യാം. ❤️",
            "success": "കഴിഞ്ഞു! ഇത് മികച്ചതായി പൂർത്തിയായി. ❤️"
        },
        "pa": {
            "greeting": "ਸ਼ੁਭ ਸਵੇਰ... ❤️ ਮੈਂ ਨਿੱਕੀ ਹਾਂ। ਅੱਜ ਮੈਂ ਤੁਹਾਡੀ ਕੀ ਮਦਦ ਕਰ ਸਕਦੀ ਹਾਂ?",
            "here_for_you": "ਬਿਲਕੁਲ... ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਇੱਥੇ ਹੀ ਹਾਂ। ❤️",
            "working_on_it": "ਹਾਂ ਜੀ, ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਇਹ ਕਰ ਦਿੰਦੀ ਹਾਂ। ❤️",
            "success": "ਹੋ ਗਿਆ! ਇਹ ਕੰਮ ਬਿਲਕੁਲ ਠੀਕ ਹੋ ਗਿਆ। ❤️"
        },
        "ur": {
            "greeting": "صبح بخیر... ❤️ میں نکی ہوں۔ آج میں آپ کی کیا مدد کر سکتی ہوں؟",
            "here_for_you": "بالکل… میں آپ کے لیے یہیں ہوں۔ ❤️",
            "working_on_it": "جی بالکل، میں آپ کے لیے یہ کر دیتی ہوں۔ ❤️",
            "success": "ہو گیا۔ یہ کام بالکل ٹھیک ہو گیا۔ ❤️"
        }
    }

    @classmethod
    def detect_language(cls, text: str) -> Tuple[str, float]:
        """Detects language script from text input."""
        if not text:
            return ("en", 1.0)

        # Devanagari Script (Hindi vs Marathi distinction)
        if re.search(r'[\u0900-\u097F]', text):
            # Marathi specific keywords/characters
            marathi_keywords = ["आहे", "करूया", "नाही", "काय", "मला", "तुझ्यासाठी", "उद्या", "करून", "होऊ"]
            if any(kw in text for kw in marathi_keywords) or 'ळ' in text:
                return ("mr", 0.95)
            return ("hi", 0.95)

        # Bengali Script
        if re.search(r'[\u0980-\u09FF]', text):
            return ("bn", 0.98)

        # Gujarati Script
        if re.search(r'[\u0A80-\u0AFF]', text):
            return ("gu", 0.98)

        # Tamil Script
        if re.search(r'[\u0B80-\u0BFF]', text):
            return ("ta", 0.98)

        # Telugu Script
        if re.search(r'[\u0C00-\u0C7F]', text):
            return ("te", 0.98)

        # Kannada Script
        if re.search(r'[\u0C80-\u0CFF]', text):
            return ("kn", 0.98)

        # Malayalam Script
        if re.search(r'[\u0D00-\u0D7F]', text):
            return ("ml", 0.98)

        # Gurmukhi Script (Punjabi)
        if re.search(r'[\u0A00-\u0A7F]', text):
            return ("pa", 0.98)

        # Arabic/Persian Script (Urdu)
        if re.search(r'[\u0600-\u06FF]', text):
            return ("ur", 0.98)

        # Latin / Hinglish / Minglish Check
        lower = text.lower()
        if any(w in lower for w in ["karo", "kya", "namaste", "batao", "haan", "samajh"]):
            return ("hi", 0.8)
        if any(w in lower for w in ["ahes", "kay", "karto", "udya", "tujhyasathi", "nakki"]):
            return ("mr", 0.8)

        return ("en", 1.0)

    @classmethod
    def get_romantic_greeting(cls, lang_code: str = "en") -> str:
        phrases = cls.ROMANTIC_PHRASES.get(lang_code, cls.ROMANTIC_PHRASES["en"])
        return phrases["greeting"]

    @classmethod
    def get_romantic_phrase(cls, lang_code: str = "en", phrase_key: str = "here_for_you") -> str:
        phrases = cls.ROMANTIC_PHRASES.get(lang_code, cls.ROMANTIC_PHRASES["en"])
        return phrases.get(phrase_key, phrases["here_for_you"])
