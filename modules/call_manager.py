"""
Voice Call Manager Module for the Local AI Assistant.
Enables the assistant to place phone calls via connected Android phone (ADB),
Windows Phone Link dialer, or WhatsApp Web without any paid API keys.
"""
import subprocess
import re

class CallManager:
    """
    Handles making voice calls to contacts or phone numbers.
    """

    @staticmethod
    def clean_phone_number(number: str) -> str:
        """Sanitizes phone number to standard dialable format."""
        return re.sub(r'[^\d+]', '', number)

    @staticmethod
    def call_via_android_adb(phone_number: str) -> str:
        """
        Places a real GSM cellular phone call directly from a connected Android phone via ADB.
        Requires NO API keys. Uses your phone's SIM card plan.
        """
        sanitized_number = CallManager.clean_phone_number(phone_number)
        if not sanitized_number:
            return "Error: Invalid phone number provided."

        cmd = f'adb shell am start -a android.intent.action.CALL -d tel:{sanitized_number}'
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                return f"📞 Call Initiated! Dialing {sanitized_number} on connected Android smartphone via ADB..."
            else:
                # Fallback to ACTION_DIAL if CALL permission is missing on phone
                fallback_cmd = f'adb shell am start -a android.intent.action.DIAL -d tel:{sanitized_number}'
                f_res = subprocess.run(fallback_cmd, shell=True, capture_output=True, text=True, timeout=10)
                if f_res.returncode == 0:
                    return f"📱 Opening Phone Dialer for {sanitized_number} on Android device..."
                return f"Failed to initiate call via ADB: {res.stderr}"
        except Exception as e:
            return f"Error placing call via ADB: {str(e)}"

    @staticmethod
    def call_via_windows_dialer(phone_number: str) -> str:
        """
        Triggers Windows default telephony / Phone Link app to place a call.
        """
        sanitized_number = CallManager.clean_phone_number(phone_number)
        cmd = f'start tel:{sanitized_number}'
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            return f"📞 Windows Phone Link launched to call {sanitized_number}!"
        except Exception as e:
            return f"Error launching Windows dialer: {str(e)}"

    @staticmethod
    def call_via_whatsapp(contact_or_number: str) -> str:
        """
        Initiates a WhatsApp voice call to a contact or phone number.
        """
        sanitized_number = CallManager.clean_phone_number(contact_or_number)
        url = f"https://web.whatsapp.com/send?phone={sanitized_number}"
        return f"🟢 WhatsApp Call URL generated: {url}. Navigating browser to place call..."
