import subprocess
import os

class CommandRunner:
    """
    Auto-executes system commands (PowerShell/CMD/Bash) autonomously on the PC.
    """

    @staticmethod
    def run_command(command: str, cwd: str = ".") -> dict:
        """Executes a local command and returns stdout, stderr, and exit code."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "exit_code": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
        except subprocess.TimeoutExpired:
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": "Command timed out after 30 seconds."
            }
        except Exception as e:
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e)
            }
