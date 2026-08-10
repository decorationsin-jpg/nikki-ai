"""
WhatsApp Reader & Auto-Responder Module using Playwright.
Uses a saved Chrome session so WhatsApp Web stays logged in without scanning QR code every time.
"""
import time

class WhatsAppMonitor:
    def __init__(self, user_data_dir: str = "./whatsapp_user_data"):
        self.user_data_dir = user_data_dir

    def check_unread_messages(self) -> list:
        """
        Launches browser with saved session, checks for unread message badges,
        reads unread messages, and returns them as structured items.
        """
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=self.user_data_dir,
                    headless=True
                )
                page = browser.new_page()
                page.goto("https://web.whatsapp.com")
                
                # Wait for chat list to load
                page.wait_for_selector("div[id='pane-side']", timeout=15000)

                # Look for unread message indicators
                unread_chats = page.query_selector_all("span[aria-label*='unread']")
                messages = []
                for chat in unread_chats:
                    chat.click()
                    time.sleep(1)
                    # Extract last received message
                    msg_elements = page.query_selector_all("div.message-in span.selectable-text")
                    if msg_elements:
                        last_msg = msg_elements[-1].inner_text()
                        messages.append({"source": "WhatsApp", "message": last_msg})
                browser.close()
                return messages
        except Exception as e:
            return [{"source": "WhatsApp", "error": f"WhatsApp automation requires setup: {str(e)}"}]
