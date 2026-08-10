"""
Nikki Self-Diagnostic System Inspector.
Checks system health, verifies all modules, dependencies, Ollama status,
and displays a 100% System Health Scorecard.
"""
import sys
import subprocess
from modules.local_llm import LocalLLM
from modules.sms_reader import SMSReader

class SystemHealthChecker:
    """
    Self-diagnostic checker for Nikki.
    """

    def run_full_diagnostic(self) -> dict:
        print("🔍 [Nikki Self-Diagnostic]: Running full system health check...")
        
        # 1. Local LLM Check
        llm_online = LocalLLM().is_available()
        
        # 2. ADB Android Connection Check
        adb_online = SMSReader.is_adb_connected()
        
        # 3. Python Packages Check
        packages = ["requests", "duckduckgo_search", "bs4", "playwright", "pyttsx3", "speech_recognition"]
        installed_packages = {}
        for pkg in packages:
            try:
                __import__(pkg)
                installed_packages[pkg] = "✅ INSTALLED"
            except ImportError:
                installed_packages[pkg] = "⚠️ NOT INSTALLED"

        score = 100 if llm_online else 80

        report = f"""
🌸 NIKKI SYSTEM HEALTH DIAGNOSTIC REPORT 🌸
===================================================
1. Local AI Brain (Ollama): {"🟢 ONLINE (100% Functional)" if llm_online else "🟡 OFFLINE (Running Rule Engine Fallback)"}
2. Android Smartphone (ADB): {"🟢 CONNECTED" if adb_online else "⚪ NOT CONNECTED (Connect phone via USB/Wi-Fi)"}
3. Python Core Runtime: {sys.version.split()[0]} ({sys.platform})

4. Key Dependencies Status:
"""
        for pkg, status in installed_packages.items():
            report += f"   - {pkg}: {status}\n"

        report += f"\nSystem Health Score: {score}/100 🌟"
        print(report)
        return {"score": score, "report": report}
