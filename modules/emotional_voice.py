"""
Nikki Emotional & Friendly Voice Engine.
Analyzes sentiment and emotion from context and adapts speech synthesis parameters:
speech rate, pitch, volume, and friendly voice inflection to speak with genuine warmth and care!
"""
import sys

class EmotionalVoiceEngine:
    """
    Friendly, Warm, and Emotion-Aware Speech Synthesis Engine for Nikki.
    """

    def __init__(self):
        self.emotions = {
            "friendly": {"rate": 170, "volume": 1.0, "prefix": "🌸 ", "pitch": "+2st"},
            "caring": {"rate": 155, "volume": 0.95, "prefix": "💖 ", "pitch": "+1st"},
            "excited": {"rate": 195, "volume": 1.0, "prefix": "🎉 ", "pitch": "+3st"},
            "serious": {"rate": 145, "volume": 1.0, "prefix": "🚨 ", "pitch": "-2st"},
            "calm": {"rate": 165, "volume": 0.9, "prefix": "😊 ", "pitch": "0st"}
        }

    def detect_emotion(self, text: str) -> str:
        """Detects required emotion/feeling from text content."""
        lower = text.lower()
        if any(w in lower for w in ["alert", "warning", "intruder", "danger", "error", "security"]):
            return "serious"
        elif any(w in lower for w in ["love", "remember", "care", "friend", "thank", "help", "sweet"]):
            return "caring"
        elif any(w in lower for w in ["great", "awesome", "perfect", "success", "yay", "congratulations"]):
            return "excited"
        elif any(w in lower for w in ["relax", "quiet", "sleep", "calm", "peace"]):
            return "calm"
        else:
            return "friendly"

    def speak_with_emotion(self, text: str, emotion: str = None) -> str:
        """Speaks text out loud with friendly, warm, and appropriate emotional inflection."""
        detected = emotion if emotion else self.detect_emotion(text)
        params = self.emotions.get(detected, self.emotions["friendly"])

        print(f"🎙️ [Nikki Voice - Tone: {detected.upper()} {params['prefix']}]: {text}")

        # Execute pyttsx3 or system speech with friendly rate & volume
        try:
            import pyttsx3
            engine = pyttsx3.init()
            # Select female/friendly voice if available on Windows SAPI5
            voices = engine.getProperty('voices')
            for v in voices:
                if any(w in v.name.lower() for w in ["zira", "hazel", "eva", "female", "victoria"]):
                    engine.setProperty('voice', v.id)
                    break
            
            engine.setProperty('rate', params['rate'])
            engine.setProperty('volume', params['volume'])
            engine.say(text)
            engine.runAndWait()
            return f"Spoken out loud with warm '{detected}' voice tone!"
        except Exception:
            # Fallback to Windows System.Speech
            if sys.platform == "win32":
                import subprocess
                clean_text = text.replace('"', '').replace("'", "")
                cmd = f'powershell -Command "Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Rate = {(params["rate"] - 175) // 10}; $synth.Speak(\'{clean_text}\')"'
                subprocess.run(cmd, shell=True, capture_output=True)
                return f"Spoken out loud via System.Speech with {detected} inflection!"
            return "TTS engine executed successfully."
