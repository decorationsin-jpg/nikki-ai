"""
Android Native Termux Engine.
Allows the AI Assistant to run DIRECTLY ON AN ANDROID PHONE using Termux & Termux:API.
No PC required! Provides direct native access to calls, SMS, camera, TTS, and sensors.
"""
import subprocess

class AndroidTermuxEngine:
    """
    Direct Termux:API wrapper for running the AI Assistant natively on Android devices.
    """

    @staticmethod
    def run_termux_cmd(cmd: str) -> str:
        """Executes a Termux API command."""
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            return res.stdout.strip() if res.returncode == 0 else res.stderr.strip()
        except Exception as e:
            return f"Termux command error: {str(e)}"

    def make_call_native(self, phone_number: str) -> str:
        """Makes a GSM phone call directly from Android phone."""
        return self.run_termux_cmd(f"termux-telephony-call '{phone_number}'")

    def send_sms_native(self, phone_number: str, message: str) -> str:
        """Sends an SMS message directly from Android phone."""
        return self.run_termux_cmd(f"termux-sms-send -n '{phone_number}' '{message}'")

    def read_sms_native(self, limit: int = 5) -> str:
        """Reads SMS inbox directly on Android phone."""
        return self.run_termux_cmd(f"termux-sms-list -l {limit}")

    def speak_native(self, text: str) -> str:
        """Speaks text out loud using Android's native Text-to-Speech engine."""
        return self.run_termux_cmd(f"termux-tts-speak '{text}'")

    def take_photo_native(self, save_path: str = "phone_photo.jpg") -> str:
        """Captures a photo using the phone's physical camera."""
        return self.run_termux_cmd(f"termux-camera-photo -c 0 {save_path}")

    def vibrate_native(self, duration_ms: int = 500) -> str:
        """Vibrates the phone."""
        return self.run_termux_cmd(f"termux-vibrate -d {duration_ms}")
