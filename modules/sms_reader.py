"""
SMS & Notification Reader using Android Debug Bridge (ADB).
Reads SMS inbox directly from a USB or Wi-Fi connected Android device without third-party APIs.
"""
import subprocess

class SMSReader:
    @staticmethod
    def is_adb_connected() -> bool:
        """Checks if an Android phone is connected via ADB."""
        try:
            res = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=5)
            lines = [l for l in res.stdout.splitlines() if l.strip()]
            return len(lines) > 1  # List of devices attached + at least one device ID
        except Exception:
            return False

    @staticmethod
    def get_latest_sms(limit: int = 5) -> list:
        """Reads latest SMS messages from Android content provider via ADB shell."""
        if not SMSReader.is_adb_connected():
            return [{"source": "SMS", "notice": "ADB device not connected. Connect phone via USB with USB Debugging enabled."}]

        cmd = f'adb shell content query --uri content://sms/inbox --projection address,body,date --sort "date DESC LIMIT {limit}"'
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                messages = []
                for line in res.stdout.splitlines():
                    if "body=" in line:
                        messages.append({"source": "SMS", "raw_content": line})
                return messages if messages else [{"source": "SMS", "notice": "No SMS found."}]
            return [{"source": "SMS", "error": res.stderr}]
        except Exception as e:
            return [{"source": "SMS", "error": str(e)}]
