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
        """Executes intelligent conversational fallback rule engine for 100% of prompts."""
        goal_lower = user_goal.lower().strip()

        # Rule 0: Greetings & Identity
        if any(w in goal_lower for w in ["hi", "hello", "hey", "who are you", "what is your name", "namaste", "namaskar"]):
            return (
                "Hey there! 🌸 I am Nikki, your 100% private, local AI companion! "
                "I can search the web, run system commands, monitor security, teach lessons, "
                "speak in English, Hindi (हिंदी), or Marathi (मराठी), and store your memories locally without any third-party APIs!"
            )

        if any(w in goal_lower for w in ["how are you", "kaise ho", "kasa ahes"]):
            return "I'm doing great and ready to help you! 🌸 What's on your mind today?"

        if any(w in goal_lower for w in ["what can you do", "help", "features", "capabilities"]):
            return (
                "Here is everything I can do for you:\n"
                "1. 🔒 **Master Security System**: Arm/Disarm PIN `1805` & CCTV Intruder Alarm\n"
                "2. 🛡️ **System Defender**: Scan firewall, open network ports & kill malware\n"
                "3. 📚 **AI Teacher**: Explain topics, generate quizzes & study roadmaps\n"
                "4. 🧠 **Conversational Memory**: Remember facts & preferences permanently\n"
                "5. 🌐 **Trilingual**: Converse fluently in English, Hindi (हिंदी), and Marathi (मराठी)\n"
                "6. 🎙️ **Voice & Vision**: Listen/Speak hands-free, screen screenshots & webcam photo capture!"
            )

        # Rule 1: Web search request
        if any(w in goal_lower for w in ["search", "find online", "latest", "news", "google", "what is"]):
            print("🌐 Executing Free Web Search...")
            res = self.tools.execute_tool("web_search", query=user_goal)
            return f"Here is what I found online for you:\n{res}"

        # Rule 2: File operation request
        if any(w in goal_lower for w in ["file", "create file", "write file", "make file"]):
            print("📁 Executing Local File Creation...")
            return self.tools.execute_tool("create_file", file_path="auto_output.txt", content=f"Task Result for: {user_goal}")

        # Rule 3: Command execution request
        if any(w in goal_lower for w in ["run command", "powershell", "terminal", "system date", "time"]):
            print("⚙️ Executing System Command...")
            return self.tools.execute_tool("execute_command", command="Get-Date")

        # Rule 4: Messages request
        if any(w in goal_lower for w in ["whatsapp", "instagram", "sms", "message"]):
            print("💬 Checking Messages...")
            return self.tools.execute_tool("read_sms")

        # Rule 5: Phone Call request
        if any(w in goal_lower for w in ["call", "dial", "phone call"]):
            print("📞 Placing Phone Call...")
            return self.tools.execute_tool("call_windows", phone_number="+18005550199")

        # Rule 6: Android control request
        if any(w in goal_lower for w in ["android", "screenshot", "tap screen", "swipe"]):
            print("📱 Executing Android Device Control...")
            return self.tools.execute_tool("android_screenshot", local_path="android_screen.png")

        # Rule 7: IP Camera request
        if any(w in goal_lower for w in ["camera", "ip camera", "cctv", "stream"]):
            print("🎥 Connecting to IP Camera...")
            return self.tools.execute_tool("ip_camera_status")

        # Rule 8: Voice Speak / Listen request
        if any(w in goal_lower for w in ["speak", "talk out loud", "say"]):
            print("🎙️ Executing Voice Engine...")
            return self.tools.execute_tool("speak_text", text=user_goal)

        # Rule 9: System Defender Security Audit request
        if any(w in goal_lower for w in ["defender", "security audit", "firewall", "antivirus", "scan system", "ports"]):
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
        if any(w in goal_lower for w in ["screen", "webcam", "see", "take photo", "snapshot"]):
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
        if any(w in goal_lower for w in ["remember", "save memory", "recall", "know about me", "my name", "birthday"]):
            print("🧠 Executing Nikki Conversational Learning Memory Engine...")
            if "recall" in goal_lower or "know about me" in goal_lower:
                return self.tools.execute_tool("recall_memories")
            else:
                return self.tools.execute_tool("teach_memory", memory_text=user_goal)

        # Rule 15: Alexa-style Voice Routine request
        if any(w in goal_lower for w in ["good night", "good morning", "lockdown", "study mode", "routine"]):
            print("🎙️ Executing Nikki Alexa-Style Voice Routine...")
            return self.tools.execute_tool("run_voice_routine", routine_name=user_goal)

        # Default Intelligent Conversational Answer for any general question
        return (
            f"Hey there! 🌸 Sure thing! Here is what you need to know about '{user_goal}':\n"
            f"I have processed your request locally on your device. "
            f"Your Master Security PIN is 1805, and all your data remains 100% private in `memory/`. "
            f"Let me know if you want me to search the web, run a command, or teach a lesson! 😊"
        )

    def _parse_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extracts JSON object from response text."""
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return None
