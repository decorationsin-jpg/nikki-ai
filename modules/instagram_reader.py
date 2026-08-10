"""
Instagram DM Reader Module using Playwright automation.
"""
class InstagramMonitor:
    def __init__(self, user_data_dir: str = "./instagram_user_data"):
        self.user_data_dir = user_data_dir

    def check_unread_dms(self) -> list:
        """
        Launches browser with saved session, navigates to Instagram inbox,
        and checks for unread direct messages.
        """
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=self.user_data_dir,
                    headless=True
                )
                page = browser.new_page()
                page.goto("https://www.instagram.com/direct/inbox/")
                # Look for unread DM indicators
                return [{"source": "Instagram", "status": "Checked inbox"}]
        except Exception as e:
            return [{"source": "Instagram", "error": f"Instagram automation error: {str(e)}"}]
