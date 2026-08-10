"""
NIKKI Operational Modes Engine.
Supports 4 Modes:
🟢 Offline Mode   - 100% Disconnected from Network.
🔵 Local Mode     - Normal local operation with optional web search.
🟡 Protected Mode - Strict human confirmation required for medium & high risk actions.
🔴 Developer Mode - Full access to terminal, python sandbox, and raw model parameters.
"""

class NikkiModeManager:
    MODES = {
        "OFFLINE": "🟢 Offline Mode (Network Disconnected, 100% Private Local)",
        "LOCAL": "🔵 Local Mode (Local Operation + Optional Web Search)",
        "PROTECTED": "🟡 Protected Mode (All Modifications Require Confirmation)",
        "DEVELOPER": "🔴 Developer Mode (Full Access to Sandbox, Logs, & Terminal)"
    }

    def __init__(self, default_mode: str = "LOCAL"):
        self.current_mode = default_mode if default_mode in self.MODES else "LOCAL"

    def set_mode(self, mode_name: str) -> str:
        mode_upper = mode_name.upper()
        if mode_upper in self.MODES:
            self.current_mode = mode_upper
            return f"Mode updated: {self.MODES[self.current_mode]}"
        return f"Invalid mode. Available modes: {list(self.MODES.keys())}"

    def get_status(self) -> dict:
        return {
            "mode": self.current_mode,
            "description": self.MODES[self.current_mode],
            "network_allowed": self.current_mode != "OFFLINE",
            "confirmation_required": self.current_mode in ["PROTECTED", "LOCAL"]
        }
