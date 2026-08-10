"""
Self-Modifying & Dynamic Skill Creator Engine for Nikki.
Allows Nikki to write new Python code modules for herself, install required dependencies,
dynamically load new tools into her active runtime memory, and update her own programming!
"""
import os
import sys
import importlib
import subprocess
from pathlib import Path

class SelfModifier:
    """
    Self-programming and dynamic skill installation engine.
    """

    def __init__(self, skills_dir: str = "custom_skills"):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        # Ensure custom_skills directory is on Python path
        if str(self.skills_dir.resolve()) not in sys.path:
            sys.path.append(str(self.skills_dir.resolve()))

    def install_pip_package(self, package_name: str) -> str:
        """Installs any required Python package automatically using pip."""
        try:
            print(f"📦 [Nikki Self-Programming]: Installing package '{package_name}' via pip...")
            res = subprocess.run([sys.executable, "-m", "pip", "install", package_name], capture_output=True, text=True, timeout=60)
            return f"Package '{package_name}' installed successfully!" if res.returncode == 0 else f"Pip install error: {res.stderr}"
        except Exception as e:
            return f"Failed to install package '{package_name}': {str(e)}"

    def write_new_skill(self, skill_name: str, code_content: str, required_packages: list = None) -> str:
        """
        Nikki writes a brand-new skill module for herself, installs dependencies,
        and saves it permanently to disk.
        """
        # 1. Install dependencies if needed
        if required_packages:
            for pkg in required_packages:
                self.install_pip_package(pkg)

        # 2. Save new code file to custom_skills directory
        safe_name = skill_name.lower().replace(" ", "_").replace(".py", "")
        file_path = self.skills_dir / f"{safe_name}.py"
        file_path.write_text(code_content, encoding='utf-8')

        print(f"🧠 [Nikki Self-Programming]: Created new skill module at {file_path.resolve()}")
        return f"New skill '{safe_name}' programmed and saved successfully at {file_path}"

    def modify_existing_code(self, target_file_path: str, new_code_content: str) -> str:
        """
        Nikki modifies or updates an existing code file on her system.
        """
        path = Path(target_file_path)
        if not path.exists():
            return f"Error: Target file '{target_file_path}' does not exist for modification."

        path.write_text(new_code_content, encoding='utf-8')
        print(f"🛠️ [Nikki Self-Programming]: Updated source code file: {path.resolve()}")
        return f"Successfully modified source code at {path.resolve()}"

    def list_custom_skills(self) -> list:
        """Lists all dynamically programmed skills Nikki has created for herself."""
        return [p.name for p in self.skills_dir.glob("*.py")]
