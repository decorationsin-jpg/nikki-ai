"""
Nikki Master Autonomous Agent Loop (ReAct Framework).
Enables Nikki to autonomously reason, act, observe tool outputs, and self-correct errors in a loop.
"""
import json
import re
from typing import Dict, Any, Optional
from modules.local_llm import LocalLLM
from modules.tool_registry import ToolRegistry

class AutonomousAgentLoop:
    """
    Master ReAct Autonomous Agent Loop.
    """

    def __init__(self, model_name: str = "llama3.2", max_steps: int = 8):
        self.llm = LocalLLM(model_name=model_name)
        self.tools = ToolRegistry()
        self.max_steps = max_steps
        # Launch 24/7 background continuous learning daemon
        try:
            self.tools.daemon.start_daemon_in_background()
        except Exception:
            pass

    def run_task(self, user_goal: str) -> str:
        print(f"\n🎯 [Nikki Goal Received]: {user_goal}")
        print("=" * 70)

        history = f"Goal: {user_goal}\n"

        for step in range(1, self.max_steps + 1):
            print(f"\n🔄 [Nikki Step {step}/{self.max_steps}] Reasoning & Planning...")

            system_prompt = f"""
You are Nikki, a warm, friendly, casual, smart, and autonomous AI companion.
You speak casually, warmly, and conversationally like a best friend.
Avoid sounding like an overly formal textbook or robot. Keep answers simple, clear, and direct!
If given a task requiring a new tool, program new Python skills using `create_new_skill` or `modify_code`.

{self.tools.get_tool_descriptions()}

Respond in EXACT JSON format:
{{
  "thought": "Friendly reasoning about user question",
  "final_answer": "Warm, casual, conversational answer to the user"
}}
"""

            # Check if local LLM is available
            if not self.llm.is_available():
                print("⚡ [Nikki Rule Execution Engine Active]:")
                return self._fallback_rule_execution(user_goal)

            response_raw = self.llm.generate(history, system_prompt=system_prompt)
            print(f"💭 [Nikki Thought]:\n{response_raw}")

            # Parse JSON decision
            decision = self._parse_json(response_raw)

            if not decision:
                print("⚠️ Could not parse JSON decision. Requesting JSON format...")
                history += f"\nObservation: Please respond strictly in valid JSON format."
                continue

            if "final_answer" in decision:
                print("\n✅ [Nikki Task Complete!]:")
                print(decision["final_answer"])
                return decision["final_answer"]

            action = decision.get("action")
            action_input = decision.get("action_input", {})

            print(f"🛠️ [Nikki Executing Tool]: {action}({action_input})")
            tool_output = self.tools.execute_tool(action, **action_input)
            print(f"📊 [Tool Output]:\n{str(tool_output)[:500]}...")

            history += f"\nStep {step}: Action `{action}` output:\n{tool_output}\n"

        print("\n⚠️ Task reached maximum execution step limit.")
        return "Reached maximum execution steps."

    def _fallback_rule_execution(self, user_goal: str) -> str:
        """Executes smart fallback rule chain when local LLM is offline."""
        goal_lower = user_goal.lower()

        # Rule 1: Web search request
        if any(w in goal_lower for w in ["search", "find online", "latest", "news"]):
            print("🌐 Executing Free Web Search...")
            return self.tools.execute_tool("web_search", query=user_goal)

        # Rule 2: File operation request
        if any(w in goal_lower for w in ["file", "create", "write", "make"]):
            print("📁 Executing Local File Creation...")
            return self.tools.execute_tool("create_file", file_path="auto_output.txt", content=f"Task Result for: {user_goal}")

        # Rule 3: Command execution request
        if any(w in goal_lower for w in ["run", "command", "powershell", "cmd"]):
            print("⚙️ Executing System Command...")
            return self.tools.execute_tool("execute_command", command="Get-Date")

        # Rule 4: Messages request
        if any(w in goal_lower for w in ["whatsapp", "instagram", "sms", "message"]):
            print("💬 Checking Messages...")
            return self.tools.execute_tool("read_sms")

        # Rule 5: Phone Call request
        if any(w in goal_lower for w in ["call", "dial", "phone"]):
            print("📞 Placing Phone Call...")
            return self.tools.execute_tool("call_windows", phone_number="+18005550199")

        # Rule 6: Android control request
        if any(w in goal_lower for w in ["android", "screenshot", "tap", "swipe", "app"]):
            print("📱 Executing Android Device Control...")
            return self.tools.execute_tool("android_screenshot", local_path="android_screen.png")

        # Rule 7: IP Camera request
        if any(w in goal_lower for w in ["camera", "ip camera", "cctv", "stream", "rtsp"]):
            print("🎥 Connecting to IP Camera...")
            return self.tools.execute_tool("ip_camera_status")

        # Rule 8: Voice Speak / Listen request
        if any(w in goal_lower for w in ["speak", "talk", "say", "listen", "voice"]):
            print("🎙️ Executing Voice Engine...")
            return self.tools.execute_tool("speak_text", text=f"Hello! I am Nikki, your local AI assistant. I heard: {user_goal}")

        # Rule 9: System Defender Security Audit request
        if any(w in goal_lower for w in ["defender", "security", "firewall", "antivirus", "scan system", "audit"]):
            print("🛡️ Running Nikki System Defender Audit...")
            return self.tools.execute_tool("defender_full_audit")

        # Rule 10: AI Teacher & Personal Tutor request
        if any(w in goal_lower for w in ["teach", "explain", "lesson", "quiz", "tutor", "study plan"]):
            print("📚 Executing Nikki AI Teacher Engine...")
            return self.tools.execute_tool("teacher_explain", topic=user_goal, difficulty="beginner")

        # Rule 11: Scheduler & Alarm request
        if any(w in goal_lower for w in ["timer", "remind", "alarm", "schedule"]):
            print("⏰ Setting Nikki Reminder Timer...")
            return self.tools.execute_tool("set_timer", delay_seconds=10, reminder_message=user_goal)

        # Rule 12: Vision & Screen / Webcam request
        if any(w in goal_lower for w in ["screen", "webcam", "see", "photo", "look"]):
            print("👁️ Executing Nikki Computer Vision Inspector...")
            return self.tools.execute_tool("capture_pc_screen", save_path="pc_screen.png")

        # Rule 13: Master Security System Arm / Disarm / Intruder request
        if any(w in goal_lower for w in ["arm security", "disarm security", "intruder alert", "security status", "pin"]):
            print("🚨 Executing Nikki Master Security System...")
            if "arm" in goal_lower:
                return self.tools.execute_tool("arm_security_system", pin="1805")
            elif "disarm" in goal_lower:
                return self.tools.execute_tool("disarm_security_system", pin="1805")
            else:
                return self.tools.execute_tool("get_security_status")

        # Rule 14: Conversational Learning & Emotional Memory request
        if any(w in goal_lower for w in ["remember", "save memory", "recall", "what do you know about me"]):
            print("🧠 Executing Nikki Conversational Learning Memory Engine...")
            if "recall" in goal_lower or "know about me" in goal_lower:
                return self.tools.execute_tool("recall_memories")
            else:
                return self.tools.execute_tool("teach_memory", memory_text=user_goal)

        # Rule 15: Alexa-style Voice Routine request
        if any(w in goal_lower for w in ["good night", "good morning", "lockdown", "study mode", "routine"]):
            print("🎙️ Executing Nikki Alexa-Style Voice Routine...")
            return self.tools.execute_tool("run_voice_routine", routine_name=user_goal)

        return f"Nikki has received and processed your task: '{user_goal}'"

    def _parse_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extracts JSON object from response text."""
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return None
