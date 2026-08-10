"""
Autonomous Agent Loop (ReAct Framework: Reason -> Act -> Observe -> Correct).
Enables the AI Assistant to autonomously execute multi-step tasks end-to-end.
"""
import json
import re
from modules.local_llm import LocalLLM
from modules.tool_registry import ToolRegistry

class AutonomousAgentLoop:
    def __init__(self, model_name: str = "llama3.2", max_steps: int = 8):
        self.llm = LocalLLM(model_name=model_name)
        self.tools = ToolRegistry()
        self.max_steps = max_steps
        # Automatically launch Nikki's 24/7 Continuous Learning Daemon in background!
        self.tools.daemon.start_daemon_in_background()

    def run_task(self, user_goal: str):
        print(f"\n🎯 [Goal Received]: {user_goal}")
        print("=" * 65)

        history = f"Goal: {user_goal}\n"

        for step in range(1, self.max_steps + 1):
            print(f"\n🔄 [Step {step}/{self.max_steps}] Thinking...")

            system_prompt = f"""
You are Nikki, a smart, powerful, friendly, self-modifying, and autonomous local AI assistant.
You operate in a ReAct loop. If you are given a task that requires a tool or feature you don't have,
you MUST write new Python code modules for yourself, install needed packages using `install_package`,
and update your own code using `create_new_skill` or `modify_code`!

{self.tools.get_tool_descriptions()}

Respond in EXACT JSON format with either a Tool Call or Final Answer:

Option 1: Tool Call
{{
  "thought": "Reasoning about what to do next or what new skill to program",
  "action": "tool_name",
  "action_input": {{ "arg_name": "arg_value" }}
}}

Option 2: Final Answer
{{
  "thought": "Goal is completed",
  "final_answer": "Complete summary of task results"
}}
"""

            # Check local LLM
            if not self.llm.is_available():
                print("⚡ [Offline Rule Execution Engine Active]:")
                return self._fallback_rule_execution(user_goal)

            response_raw = self.llm.generate(history, system_prompt=system_prompt)
            print(f"💭 [Thought & Decision]:\n{response_raw}")

            # Try parsing JSON decision
            decision = self._parse_json(response_raw)

            if not decision:
                print("⚠️ Could not parse JSON format from local LLM. Re-prompting...")
                history += f"\nObservation: Please respond strictly in valid JSON format."
                continue

            if "final_answer" in decision:
                print("\n✅ [Task Complete!]:")
                print(decision["final_answer"])
                return decision["final_answer"]

            action = decision.get("action")
            action_input = decision.get("action_input", {})

            print(f"🛠️ [Executing Tool]: {action}({action_input})")
            tool_output = self.tools.execute_tool(action, **action_input)
            print(f"📊 [Tool Output]:\n{tool_output[:500]}...")

            history += f"\nStep {step}: Action `{action}` output:\n{tool_output}\n"

        print("\n⚠️ Task reached maximum step limit.")
        return "Reached maximum execution steps."

    def _fallback_rule_execution(self, user_goal: str) -> str:
        """Executes smart fallback rule chain when Ollama is offline."""
        goal_lower = user_goal.lower()

        # Rule 1: Web search request
        if any(w in goal_lower for w in ["search", "find online", "latest", "news"]):
            print("🌐 Executing Free Web Search...")
            results = self.tools.execute_tool("web_search", query=user_goal)
            print(f"Results: {results}")

        # Rule 2: File operation request
        if any(w in goal_lower for w in ["file", "create", "write", "make"]):
            print("📁 Executing Local File Creation...")
            res = self.tools.execute_tool("create_file", file_path="auto_output.txt", content=f"Task Result for: {user_goal}")
            print(res)

        # Rule 3: Command execution request
        if any(w in goal_lower for w in ["run", "command", "powershell", "cmd"]):
            print("⚙️ Executing System Command...")
            res = self.tools.execute_tool("execute_command", command="Get-Date")
            print(res)

        # Rule 4: Messages request
        if any(w in goal_lower for w in ["whatsapp", "instagram", "sms", "message"]):
            print("💬 Checking Messages...")
            sms = self.tools.execute_tool("read_sms")
            print(f"SMS Status: {sms}")

        # Rule 5: Phone Call request
        if any(w in goal_lower for w in ["call", "dial", "phone"]):
            print("📞 Placing Phone Call...")
            call_res = self.tools.execute_tool("call_windows", phone_number="+1234567890")
            print(f"Call Result: {call_res}")

        # Rule 6: Android control request
        if any(w in goal_lower for w in ["android", "screenshot", "tap", "swipe", "app"]):
            print("📱 Executing Android Device Control...")
            res = self.tools.execute_tool("android_screenshot", local_path="android_screen.png")
            print(f"Android Action: {res}")

        # Rule 7: IP Camera request
        if any(w in goal_lower for w in ["camera", "ip camera", "cctv", "stream", "rtsp"]):
            print("🎥 Connecting to IP Camera...")
            cam_res = self.tools.execute_tool("ip_camera_status")
            print(f"IP Camera Status: {cam_res}")

        # Rule 8: Voice Speak / Listen request
        if any(w in goal_lower for w in ["speak", "talk", "say", "listen", "voice"]):
            print("🎙️ Executing Voice Engine...")
            v_res = self.tools.execute_tool("speak_text", text=f"Hello! I am Nikki, your local AI assistant. I heard: {user_goal}")
            print(f"Voice Output: {v_res}")

        # Rule 9: System Defender Security Audit request
        if any(w in goal_lower for w in ["defender", "security", "firewall", "antivirus", "scan system", "audit"]):
            print("🛡️ Running Nikki System Defender Audit...")
            audit_res = self.tools.execute_tool("defender_full_audit")
            print(f"System Security Audit Output:\n{audit_res}")

        # Rule 10: AI Teacher & Personal Tutor request
        if any(w in goal_lower for w in ["teach", "explain", "lesson", "quiz", "tutor", "study plan"]):
            print("📚 Executing Nikki AI Teacher Engine...")
            lesson_res = self.tools.execute_tool("teacher_explain", topic=user_goal, difficulty="beginner")
            print(f"Teacher Lesson Output:\n{lesson_res}")

        # Rule 11: Scheduler & Alarm request
        if any(w in goal_lower for w in ["timer", "remind", "alarm", "schedule"]):
            print("⏰ Setting Nikki Reminder Timer...")
            t_res = self.tools.execute_tool("set_timer", delay_seconds=10, reminder_message=user_goal)
            print(f"Scheduler Output: {t_res}")

        # Rule 12: Vision & Screen / Webcam request
        if any(w in goal_lower for w in ["screen", "webcam", "see", "photo", "look"]):
            print("👁️ Executing Nikki Computer Vision Inspector...")
            v_res = self.tools.execute_tool("capture_pc_screen", save_path="pc_screen.png")
            print(f"Vision Output: {v_res}")

        # Rule 13: Master Security System Arm / Disarm / Intruder request
        if any(w in goal_lower for w in ["arm security", "disarm security", "intruder alert", "security status", "pin"]):
            print("🚨 Executing Nikki Master Security System...")
            if "arm" in goal_lower:
                s_res = self.tools.execute_tool("arm_security_system", pin="1805")
            elif "disarm" in goal_lower:
                s_res = self.tools.execute_tool("disarm_security_system", pin="1805")
            else:
                s_res = self.tools.execute_tool("get_security_status")
            print(f"Security System Output:\n{s_res}")

        # Rule 14: Conversational Learning & Emotional Memory request
        if any(w in goal_lower for w in ["remember", "save memory", "recall", "what do you know about me"]):
            print("🧠 Executing Nikki Conversational Learning Memory Engine...")
            if "recall" in goal_lower or "know about me" in goal_lower:
                m_res = self.tools.execute_tool("recall_memories")
            else:
                m_res = self.tools.execute_tool("teach_memory", memory_text=user_goal)
            print(f"Memory Output:\n{m_res}")

        return "Task processed via local rule execution engine!"

    def _parse_json(self, text: str) -> dict:
        """Extracts JSON object from text."""
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return None
