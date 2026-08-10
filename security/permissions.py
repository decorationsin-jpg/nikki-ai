"""
NIKKI Security Layer & Permission System.
Enforces 4 Permission Levels (Level 0 Safe to Level 3 Dangerous).
"""

from typing import Dict, Any

class SecurityPermissionEngine:
    LEVEL_0_SAFE = 0       # Read docs, calculate, Q&A (No confirmation)
    LEVEL_1_LOW_RISK = 1   # Create notes, write files, rename files (No confirmation)
    LEVEL_2_MEDIUM = 2     # Move files, install software, run scripts (Confirmation required)
    LEVEL_3_DANGEROUS = 3  # Delete files, format disk, security settings (Mandatory PIN confirmation)

    TOOL_PERMISSIONS = {
        "read_file": LEVEL_0_SAFE,
        "search_memory": LEVEL_0_SAFE,
        "calculate": LEVEL_0_SAFE,
        "web_search": LEVEL_0_SAFE,
        "create_note": LEVEL_1_LOW_RISK,
        "create_file": LEVEL_1_LOW_RISK,
        "rename_file": LEVEL_1_LOW_RISK,
        "move_file": LEVEL_2_MEDIUM,
        "execute_script": LEVEL_2_MEDIUM,
        "open_application": LEVEL_2_MEDIUM,
        "delete_file": LEVEL_3_DANGEROUS,
        "format_disk": LEVEL_3_DANGEROUS,
        "run_privileged_cmd": LEVEL_3_DANGEROUS
    }

    @classmethod
    def evaluate_permission(cls, tool_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        level = cls.TOOL_PERMISSIONS.get(tool_name, cls.LEVEL_2_MEDIUM)
        
        requires_confirmation = level >= cls.LEVEL_2_MEDIUM
        requires_pin = level >= cls.LEVEL_3_DANGEROUS

        warning_message = ""
        if level == cls.LEVEL_2_MEDIUM:
            warning_message = f"⚠️ Low-Risk Action Request: '{tool_name}' requires your confirmation."
        elif level == cls.LEVEL_3_DANGEROUS:
            warning_message = f"🛑 Dangerous Action Request: '{tool_name}' requires Master Security PIN confirmation!"

        return {
            "tool_name": tool_name,
            "permission_level": level,
            "requires_confirmation": requires_confirmation,
            "requires_pin": requires_pin,
            "warning": warning_message,
            "allowed_by_default": level < cls.LEVEL_2_MEDIUM
        }
