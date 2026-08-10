"""
Full Android Device Control Engine via ADB (Android Debug Bridge).
Provides 100% full remote control over connected Android devices:
screen capture, UI automation, tapping, swiping, app launching, key events, and system inspection.
"""
import subprocess
import time

class AndroidController:
    """
    Complete Android ADB Remote Control Engine.
    Requires USB Debugging enabled on the Android device.
    """

    @staticmethod
    def run_adb(command: str) -> dict:
        """Helper to run ADB shell commands."""
        full_cmd = f"adb {command}"
        try:
            res = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=15)
            return {
                "success": res.returncode == 0,
                "stdout": res.stdout.strip(),
                "stderr": res.stderr.strip()
            }
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e)}

    def capture_screenshot(self, local_save_path: str = "android_screen.png") -> str:
        """Captures a high-res screenshot of the Android screen and pulls it to PC."""
        res1 = self.run_adb("shell screencap -p /sdcard/screencap.png")
        if not res1["success"]:
            return f"Failed to capture screenshot: {res1['stderr']}"

        res2 = self.run_adb(f"pull /sdcard/screencap.png {local_save_path}")
        if res2["success"]:
            return f"📸 Screenshot saved successfully to: {local_save_path}"
        return f"Failed to pull screenshot: {res2['stderr']}"

    def tap_screen(self, x: int, y: int) -> str:
        """Simulates a screen touch at coordinates (X, Y)."""
        res = self.run_adb(f"shell input tap {x} {y}")
        return f"👉 Tapped screen at ({x}, {y})" if res["success"] else res["stderr"]

    def swipe_screen(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> str:
        """Simulates a swipe gesture from (X1, Y1) to (X2, Y2)."""
        res = self.run_adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration_ms}")
        return f"👆 Swiped from ({x1},{y1}) to ({x2},{y2})" if res["success"] else res["stderr"]

    def type_text(self, text: str) -> str:
        """Types text into the currently active text field on Android."""
        # Replace spaces with %s for ADB input command
        formatted_text = text.replace(" ", "%s")
        res = self.run_adb(f"shell input text '{formatted_text}'")
        return f"⌨️ Typed text: '{text}'" if res["success"] else res["stderr"]

    def press_button(self, button_name: str) -> str:
        """
        Presses physical or system buttons.
        Supported: HOME, BACK, POWER, VOLUME_UP, VOLUME_DOWN, ENTER, APP_SWITCH
        """
        key_map = {
            "HOME": "3",
            "BACK": "4",
            "POWER": "26",
            "VOLUME_UP": "24",
            "VOLUME_DOWN": "25",
            "ENTER": "66",
            "APP_SWITCH": "187"
        }
        key_code = key_map.get(button_name.upper(), button_name)
        res = self.run_adb(f"shell input keyevent {key_code}")
        return f"🔘 Pressed button: {button_name}" if res["success"] else res["stderr"]

    def launch_app(self, package_name: str) -> str:
        """Launches any installed Android application by package name."""
        res = self.run_adb(f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
        return f"🚀 Launched app: {package_name}" if res["success"] else res["stderr"]

    def list_installed_apps(self) -> str:
        """Lists all installed applications on the Android phone."""
        res = self.run_adb("shell pm list packages")
        return res["stdout"] if res["success"] else res["stderr"]

    def get_ui_layout_xml(self) -> str:
        """Dumps current screen UI hierarchy XML for element inspection."""
        self.run_adb("shell uiautomator dump /sdcard/window_dump.xml")
        res = self.run_adb("shell cat /sdcard/window_dump.xml")
        return res["stdout"][:2000] if res["success"] else res["stderr"]
