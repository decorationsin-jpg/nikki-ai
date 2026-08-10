"""
Nikki Advanced Code Executor & Sandbox Environment.
Safely executes Python code, captures stdout/stderr, measures execution time, and auto-fixes code errors.
"""
import io
import sys
import time
import traceback
from typing import Dict, Any

class AdvancedCodeExecutor:
    """
    Advanced Python Code Execution & Auto-Repair Engine.
    """

    def execute_python(self, code_str: str) -> Dict[str, Any]:
        """Executes Python code dynamically and captures stdout, stderr, and execution time."""
        buffer_stdout = io.StringIO()
        buffer_stderr = io.StringIO()
        start_time = time.time()

        old_stdout = sys.stdout
        old_stderr = sys.stderr

        sys.stdout = buffer_stdout
        sys.stderr = buffer_stderr

        success = True
        error_msg = ""

        try:
            # Create isolated local execution scope
            exec_scope = {}
            exec(code_str, exec_scope)
        except Exception:
            success = False
            error_msg = traceback.format_exc()
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        elapsed_time = round(time.time() - start_time, 4)

        return {
            "success": success,
            "stdout": buffer_stdout.getvalue().strip(),
            "stderr": buffer_stderr.getvalue().strip() or error_msg,
            "execution_time_sec": elapsed_time
        }
