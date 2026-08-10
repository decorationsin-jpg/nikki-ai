"""
Nikki Scheduler & Reminder Engine.
Enables Nikki to set one-time reminders, background timers, daily alarm clocks,
and recurring automated task schedules using Python threading and cron logic.
"""
import time
import threading
import json
from pathlib import Path

class NikkiScheduler:
    """
    Automated Reminder & Cron Scheduler Engine.
    """

    def __init__(self, schedule_file: str = "memory/schedules.json"):
        self.schedule_file = Path(schedule_file)
        self.schedule_file.parent.mkdir(parents=True, exist_ok=True)
        self.active_timers = []
        self._init_schedule_store()

    def _init_schedule_store(self):
        if not self.schedule_file.exists():
            self.schedule_file.write_text(json.dumps([], indent=2), encoding='utf-8')

    def set_timer(self, delay_seconds: int, reminder_message: str) -> str:
        """Sets a one-time reminder timer that notifies the user and speaks out loud."""
        print(f"⏰ [Nikki Scheduler]: Setting timer for {delay_seconds} seconds: '{reminder_message}'")

        def timer_job():
            time.sleep(delay_seconds)
            print(f"\n🔔 [REMINDER ALARM]: {reminder_message}")
            try:
                from modules.voice_engine import VoiceEngine
                VoiceEngine().speak(f"Reminder alarm: {reminder_message}")
            except Exception:
                pass

        t = threading.Thread(target=timer_job, daemon=True)
        t.start()
        self.active_timers.append({"message": reminder_message, "delay_sec": delay_seconds})
        return f"⏰ Timer set successfully! Nikki will remind you in {delay_seconds} seconds: '{reminder_message}'"

    def list_reminders(self) -> str:
        """Lists active reminders and scheduled timers."""
        return str(self.active_timers) if self.active_timers else "No active timers currently scheduled."
