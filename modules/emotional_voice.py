"""
Nikki Emotional Voice & Sentiment Reactivity Engine.
Analyzes sentiment and emotion from context and adapts speech synthesis parameters:
speech rate, pitch, volume, and inflection to speak with genuine feelings!
"""
import sys

class EmotionalVoiceEngine:
    """
    Emotion-Aware Speech Synthesis Engine for Nikki.
    """

    def __init__(self):
        self.emotions = {
            "happy": {"rate": 195, "volume": 1.0, "prefix": "💖 "},
            "caring": {"rate": 160, "volume": 0.9, "prefix": "🌸 "},
            "excited": {"rate": 210, "volume": 1.0, "prefix": "🎉 "},
            "serious": {"rate": 150, "volume": 1.0, "prefix": "🚨 "},
            "calm": {"rate": 170, "volume": 0.85, "prefix": "😊 "}
        }

    def detect_emotion(self, text: str) -> str:
        """Detects required emotion/feeling from text content."""
        lower = text.lower()
        if any(w in lower for w in ["alert", "warning", "intruder", "danger", "error", "security"]):
            return "serious"
        elif any(w in lower for w in ["love", "remember", "care", "friend", "thank", "happy"]):
            return "caring"
        elif any(w in lower for w in ["great", "awesome", "perfect", "success", "yay", "congratulations"]):
            return "excited"
        elif any(w in lower for w in ["relax", "quiet", "sleep", "calm", "peace"]):
            return "calm"
        else:
            return "happy"

    def speak_with_emotion(self, text: str, emotion: str = None) -> str:
        """Speaks text out loud with appropriate emotional inflection, rate, and volume."""
        detected = emotion if emotion else self.detect_emotion(text)
        params = self.emotions.get(detected, self.emotions["happy"])

        print(f"🎙️ [Nikki Emotional Voice - Feeling: {detected.upper()} {params['prefix']}]: {text}")

        # Execute pyttsx3 or system speech with modulated rate & volume
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', params['rate'])
            engine.setProperty('volume', params['volume'])
            engine.say(text)
            engine.runAndWait()
            return f"Spoken out loud with '{detected}' emotional feeling!"
        except Exception:
            # Fallback to Windows System.Speech
            if sys.platform == "win32":
                import subprocess
                clean_text = text.replace('"', '').replace("'", "")
                cmd = f'powershell -Command "Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Rate = {(params["rate"] - 175) // 10}; $synth.Speak(\'{clean_text}\')"'
                subprocess.run(cmd, shell=True, capture_output=True)
                return f"Spoken out loud via System.Speech with {detected} inflection!"
            return "TTS engine error."
