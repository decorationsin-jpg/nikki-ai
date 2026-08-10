"""
Unified Tool Registry for the Local AI Assistant.
Provides all executable capabilities as clean Python functions.
"""
from modules.web_search import FreeWebSearch
from modules.file_manager import LocalFileManager
from modules.command_runner import CommandRunner
from modules.sms_reader import SMSReader
from modules.whatsapp_reader import WhatsAppMonitor
from modules.instagram_reader import InstagramMonitor
from modules.call_manager import CallManager
from modules.android_controller import AndroidController
from modules.ip_camera import IPCameraManager
from modules.voice_engine import VoiceEngine
from modules.self_modifier import SelfModifier
from modules.continuous_learning_daemon import ContinuousLearningDaemon
from modules.system_defender import SystemDefender
from modules.ai_teacher import AITeacher
from modules.scheduler import NikkiScheduler
from modules.vision_inspector import VisionInspector
from modules.master_security_system import MasterSecuritySystem
from modules.health_checker import SystemHealthChecker
from modules.memory_engine import MemoryEngine
from modules.emotional_voice import EmotionalVoiceEngine
from modules.android_termux_engine import AndroidTermuxEngine
from modules.master_assistant_hub import MasterAssistantHub
from modules.trilingual_engine import TrilingualEngine
from modules.responsible_ai import ResponsibleAIEngine
from modules.advanced_code_executor import AdvancedCodeExecutor
from modules.deep_web_intelligence import DeepWebIntelligence
from modules.system_optimizer import SystemOptimizer

class ToolRegistry:
    def __init__(self):
        self.web = FreeWebSearch()
        self.files = LocalFileManager()
        self.cmd = CommandRunner()
        self.sms = SMSReader()
        self.whatsapp = WhatsAppMonitor()
        self.instagram = InstagramMonitor()
        self.calls = CallManager()
        self.android = AndroidController()
        self.camera = IPCameraManager()
        self.voice = VoiceEngine()
        self.modifier = SelfModifier()
        self.daemon = ContinuousLearningDaemon()
        self.defender = SystemDefender()
        self.teacher = AITeacher()
        self.scheduler = NikkiScheduler()
        self.vision = VisionInspector()
        self.sec_sys = MasterSecuritySystem()
        self.health = SystemHealthChecker()
        self.mem_eng = MemoryEngine()
        self.emo_voice = EmotionalVoiceEngine()
        self.termux = AndroidTermuxEngine()
        self.hub = MasterAssistantHub()
        self.tri_lang = TrilingualEngine()
        self.resp_ai = ResponsibleAIEngine()
        self.executor = AdvancedCodeExecutor()
        self.deep_web = DeepWebIntelligence()
        self.optimizer = SystemOptimizer()

    def get_tool_descriptions(self) -> str:
        return """
Available Tools:
1. web_search(query): Search DuckDuckGo for free (no API key).
2. fetch_webpage(url): Extract readable text from any website URL.
3. create_file(file_path, content): Create or overwrite a local file.
4. read_file(file_path): Read content from a local file.
5. execute_command(command): Run a system terminal command (PowerShell/Bash).
6. read_whatsapp(): Check unread WhatsApp Web messages.
7. read_instagram(): Check unread Instagram Direct Messages.
8. read_sms(): Read SMS inbox from connected Android phone via ADB.
9. make_phone_call(phone_number): Place a GSM phone call via connected Android phone (ADB).
10. call_whatsapp(phone_number): Initiate a WhatsApp call to a number.
11. call_windows(phone_number): Launch Windows Phone Link dialer for a number.
12. android_screenshot(local_path): Capture high-res screenshot of connected Android screen.
13. android_tap(x, y): Touch screen at (X, Y) coordinates.
14. android_type(text): Type text into active field on Android phone.
15. android_launch_app(package_name): Launch an app on Android device.
16. android_press_button(button_name): Press HOME, BACK, POWER, or VOLUME buttons.
17. ip_camera_snapshot(camera_url): Capture JPEG frame from local IP camera stream.
18. ip_camera_status(camera_url): Check if IP camera stream is online.
19. speak_text(text): Speak given text out loud using local offline TTS engine.
20. listen_voice(): Listen to user microphone and transcribe voice input.
21. create_new_skill(skill_name, code_content, required_packages): Nikki writes a new Python skill for herself and installs dependencies.
22. modify_code(target_file_path, new_code_content): Nikki updates or fixes her own source code files.
23. install_package(package_name): Install any Python package automatically using pip.
24. list_custom_skills(): List all custom skills Nikki has programmed for herself.
25. start_247_learning(): Launch Nikki's 24/7 background continuous learning daemon.
26. stop_247_learning(): Stop Nikki's 24/7 background learning daemon.
27. get_memory_summary(): Read Nikki's long-term memory database and learned topics.
28. defender_scan_processes(): Audit active system processes for malware or high usage.
29. defender_scan_ports(): Scan active network connections and listening ports.
30. defender_check_security(): Audit Windows Defender & Firewall security status.
31. defender_kill_process(process_name_or_id): Terminate an unauthorized process.
32. defender_full_audit(): Perform a full system security audit report.
33. teacher_explain(topic, difficulty): Nikki explains any topic clearly with examples and analogies.
34. teacher_quiz(topic, num_questions): Nikki generates an interactive practice quiz.
35. teacher_grade(question, student_answer): Nikki grades student answers and provides feedback.
36. teacher_study_plan(subject, days): Nikki generates a structured learning roadmap.
37. set_timer(delay_seconds, reminder_message): Nikki sets a timer/reminder that alerts you out loud.
38. list_reminders(): List all active scheduled timers and reminders.
39. capture_pc_screen(save_path): Capture a full high-res screenshot of your PC desktop.
40. capture_webcam_photo(save_path): Capture a photo snapshot from your PC's webcam.
41. arm_security_system(pin): ARM Nikki's Master CCTV Intruder Alarm & Security System (Requires PIN).
42. disarm_security_system(pin): DISARM Nikki's Master Security System (Requires PIN).
43. set_master_pin(old_pin, new_pin): Change Nikki's Master Security PIN passcode.
44. trigger_intruder_alert(location): Sound emergency siren, capture intruder photo, and alert user.
45. get_security_status(): Inspect full status of Nikki's Master Security System.
46. run_system_diagnostic(): Run Nikki's self-diagnostic system health check.
47. teach_fact(key, value): Teach Nikki a personal fact (e.g. birthday, name, preference).
48. teach_memory(memory_text): Teach Nikki a custom memory or rule to save permanently.
49. recall_memories(query): Recall all saved facts and conversational memories.
50. speak_with_emotion(text, emotion): Speak text out loud with emotional feelings (happy, caring, excited, serious, calm).
51. termux_call(phone_number): Make a GSM phone call directly on Android phone via Termux API.
52. termux_sms_send(phone_number, message): Send an SMS directly on Android phone via Termux API.
53. termux_sms_read(limit): Read SMS inbox directly on Android phone via Termux API.
54. termux_speak(text): Speak out loud using native Android TTS via Termux API.
55. termux_photo(save_path): Take a camera photo directly on Android phone via Termux API.
56. termux_vibrate(duration_ms): Vibrate Android phone via Termux API.
57. run_voice_routine(routine_name): Execute Alexa-style smart voice routine ('good night', 'good morning', 'lockdown', 'study').
58. detect_language(text): Detect whether user text/voice is English, Hindi (हिंदी), or Marathi (मराठी).
59. speak_trilingual(text, language): Speak out loud in English, Hindi (हिंदी), or Marathi (मराठी).
60. rag_query(query): Perform Retrieval-Augmented Generation (RAG) with source citations, confidence scoring, and anti-hallucination guardrails.
61. execute_python(code_str): Dynamically execute Python code in an isolated sandbox environment and capture stdout/stderr.
62. deep_research(topic): Generate a deep research briefing synthesizing Wikipedia, GitHub repos, and web articles.
63. optimize_memory(): Free unused RAM and force garbage collection cleanup.
64. get_hardware_telemetry(): Fetch detailed CPU, RAM, and Disk metrics.
"""

    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """Executes a requested tool by name with arguments."""
        try:
            if tool_name == "web_search":
                return str(self.web.search(kwargs.get("query", "")))
            elif tool_name == "fetch_webpage":
                return self.web.fetch_page_text(kwargs.get("url", ""))
            elif tool_name == "create_file":
                return self.files.write_file(kwargs.get("file_path", ""), kwargs.get("content", ""))
            elif tool_name == "read_file":
                return self.files.read_file(kwargs.get("file_path", ""))
            elif tool_name == "execute_command":
                res = self.cmd.run_command(kwargs.get("command", ""))
                return f"Exit Code: {res['exit_code']}\nStdout: {res['stdout']}\nStderr: {res['stderr']}"
            elif tool_name == "read_whatsapp":
                return str(self.whatsapp.check_unread_messages())
            elif tool_name == "read_instagram":
                return str(self.instagram.check_unread_dms())
            elif tool_name == "read_sms":
                return str(self.sms.get_latest_sms())
            elif tool_name == "make_phone_call":
                return self.calls.call_via_android_adb(kwargs.get("phone_number", ""))
            elif tool_name == "call_whatsapp":
                return self.calls.call_via_whatsapp(kwargs.get("phone_number", ""))
            elif tool_name == "call_windows":
                return self.calls.call_via_windows_dialer(kwargs.get("phone_number", ""))
            elif tool_name == "android_screenshot":
                return self.android.capture_screenshot(kwargs.get("local_path", "android_screen.png"))
            elif tool_name == "android_tap":
                return self.android.tap_screen(kwargs.get("x", 500), kwargs.get("y", 1000))
            elif tool_name == "android_type":
                return self.android.type_text(kwargs.get("text", ""))
            elif tool_name == "android_launch_app":
                return self.android.launch_app(kwargs.get("package_name", ""))
            elif tool_name == "android_press_button":
                return self.android.press_button(kwargs.get("button_name", "HOME"))
            elif tool_name == "ip_camera_snapshot":
                return self.camera.capture_snapshot(kwargs.get("camera_url", None))
            elif tool_name == "ip_camera_status":
                return self.camera.check_camera_status(kwargs.get("camera_url", None))
            elif tool_name == "speak_text":
                return self.emo_voice.speak_with_emotion(kwargs.get("text", ""))
            elif tool_name == "listen_voice":
                return self.voice.listen()
            elif tool_name == "create_new_skill":
                return self.modifier.write_new_skill(
                    kwargs.get("skill_name", ""),
                    kwargs.get("code_content", ""),
                    kwargs.get("required_packages", None)
                )
            elif tool_name == "modify_code":
                return self.modifier.modify_existing_code(
                    kwargs.get("target_file_path", ""),
                    kwargs.get("new_code_content", "")
                )
            elif tool_name == "install_package":
                return self.modifier.install_pip_package(kwargs.get("package_name", ""))
            elif tool_name == "list_custom_skills":
                return str(self.modifier.list_custom_skills())
            elif tool_name == "start_247_learning":
                return self.daemon.start_daemon_in_background()
            elif tool_name == "stop_247_learning":
                return self.daemon.stop_daemon()
            elif tool_name == "get_memory_summary":
                return str(self.daemon.load_memory())
            elif tool_name == "defender_scan_processes":
                return str(self.defender.scan_running_processes())
            elif tool_name == "defender_scan_ports":
                return self.defender.scan_open_network_ports()
            elif tool_name == "defender_check_security":
                return self.defender.check_firewall_and_antivirus_status()
            elif tool_name == "defender_kill_process":
                return self.defender.terminate_process(kwargs.get("process_name_or_id", ""))
            elif tool_name == "defender_full_audit":
                return self.defender.audit_system_security()
            elif tool_name == "teacher_explain":
                return self.teacher.explain_concept(kwargs.get("topic", ""), kwargs.get("difficulty", "beginner"))
            elif tool_name == "teacher_quiz":
                return self.teacher.create_quiz(kwargs.get("topic", ""), kwargs.get("num_questions", 3))
            elif tool_name == "teacher_grade":
                return self.teacher.grade_answer(kwargs.get("question", ""), kwargs.get("student_answer", ""))
            elif tool_name == "teacher_study_plan":
                return self.teacher.generate_study_plan(kwargs.get("subject", ""), kwargs.get("days", 7))
            elif tool_name == "set_timer":
                return self.scheduler.set_timer(int(kwargs.get("delay_seconds", 10)), kwargs.get("reminder_message", ""))
            elif tool_name == "list_reminders":
                return self.scheduler.list_reminders()
            elif tool_name == "capture_pc_screen":
                return self.vision.capture_pc_screen(kwargs.get("save_path", "pc_screen.png"))
            elif tool_name == "capture_webcam_photo":
                return self.vision.capture_webcam_photo(kwargs.get("save_path", "webcam_photo.jpg"))
            elif tool_name == "arm_security_system":
                return self.sec_sys.arm_security_system(kwargs.get("pin", "1805"))
            elif tool_name == "disarm_security_system":
                return self.sec_sys.disarm_security_system(kwargs.get("pin", "1805"))
            elif tool_name == "set_master_pin":
                return self.sec_sys.set_master_pin(kwargs.get("old_pin", "1805"), kwargs.get("new_pin", "1805"))
            elif tool_name == "trigger_intruder_alert":
                return self.sec_sys.trigger_intruder_alert(kwargs.get("location", "Front Entrance"))
            elif tool_name == "get_security_status":
                return self.sec_sys.get_security_status()
            elif tool_name == "run_system_diagnostic":
                return str(self.health.run_full_diagnostic())
            elif tool_name == "teach_fact":
                return self.mem_eng.teach_fact(kwargs.get("key", ""), kwargs.get("value", ""))
            elif tool_name == "teach_memory":
                return self.mem_eng.teach_memory(kwargs.get("memory_text", ""))
            elif tool_name == "recall_memories":
                return self.mem_eng.recall_memories(kwargs.get("query", ""))
            elif tool_name == "speak_with_emotion":
                return self.emo_voice.speak_with_emotion(kwargs.get("text", ""), kwargs.get("emotion", None))
            elif tool_name == "termux_call":
                return self.termux.make_call_native(kwargs.get("phone_number", ""))
            elif tool_name == "termux_sms_send":
                return self.termux.send_sms_native(kwargs.get("phone_number", ""), kwargs.get("message", ""))
            elif tool_name == "termux_sms_read":
                return self.termux.read_sms_native(kwargs.get("limit", 5))
            elif tool_name == "termux_speak":
                return self.termux.speak_native(kwargs.get("text", ""))
            elif tool_name == "termux_photo":
                return self.termux.take_photo_native(kwargs.get("save_path", "phone_photo.jpg"))
            elif tool_name == "termux_vibrate":
                return self.termux.vibrate_native(kwargs.get("duration_ms", 500))
            elif tool_name == "run_voice_routine":
                return self.hub.run_routine(kwargs.get("routine_name", "good night"))
            elif tool_name == "detect_language":
                return self.tri_lang.detect_language(kwargs.get("text", ""))
            elif tool_name == "speak_trilingual":
                return self.tri_lang.speak_trilingual(kwargs.get("text", ""), kwargs.get("language", "english"))
            elif tool_name == "rag_query":
                return str(self.resp_ai.rag_query(kwargs.get("query", "")))
            elif tool_name == "execute_python":
                return str(self.executor.execute_python(kwargs.get("code_str", "")))
            elif tool_name == "deep_research":
                return self.deep_web.build_deep_research_briefing(kwargs.get("topic", ""))
            elif tool_name == "optimize_memory":
                return self.optimizer.optimize_memory()
            elif tool_name == "get_hardware_telemetry":
                return str(self.optimizer.get_hardware_telemetry())
            else:
                return f"Error: Unknown tool '{tool_name}'"
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
