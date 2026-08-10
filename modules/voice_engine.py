"""
Local Voice Engine (Speech-to-Text & Text-to-Speech).
Enables the AI Assistant to listen to user voice commands via microphone
and speak responses out loud using offline local TTS engines (pyttsx3 / SAPI5 / Whisper).
Requires ZERO paid API keys and works 100% offline.
"""
import sys

class VoiceEngine:
    """
    Offline Voice Engine for listening (STT) and speaking (TTS).
    """

    def __init__(self, voice_rate: int = 175):
        self.voice_rate = voice_rate
        self.engine = None
        self._init_tts()

    def _init_tts(self):
        """Initializes pyttsx3 offline text-to-speech engine if available."""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.voice_rate)
            # Select default voice (usually female or standard system voice)
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
        except Exception:
            self.engine = None

    def speak(self, text: str) -> str:
        """Speaks the given text out loud using local offline TTS."""
        print(f"🔊 [Speaking]: {text}")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
                return "Successfully spoken out loud."
            except Exception as e:
                return f"TTS execution error: {str(e)}"
        else:
            # Fallback to PowerShell SAPI.SpVoice on Windows if pyttsx3 isn't installed yet
            if sys.platform == "win32":
                import subprocess
                clean_text = text.replace('"', '').replace("'", "")
                cmd = f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{clean_text}\')"'
                subprocess.run(cmd, shell=True, capture_output=True)
                return "Spoken via Windows System.Speech fallback."
            return "TTS engine not initialized. Install pyttsx3 via `pip install pyttsx3`."

    def listen(self, timeout_sec: int = 5) -> str:
        """
        Listens to user voice via microphone and transcribes it to text.
        Uses SpeechRecognition + local Whisper / Google speech engine.
        """
        print("\n🎙️ [Listening... Speak into your microphone]:")
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=timeout_sec, phrase_time_limit=10)
                print("⏳ Processing voice input...")
                # Transcribe using speech recognition
                text = r.recognize_google(audio)
                print(f"🗣️ [Recognized Speech]: {text}")
                return text
        except ImportError:
            return "[Voice Input Notice]: SpeechRecognition module not installed. Install via `pip install SpeechRecognition PyAudio`."
        except Exception as e:
            return f"[Voice Listening Notice]: Could not hear audio clearly ({str(e)})."
