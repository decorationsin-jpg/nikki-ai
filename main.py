"""
Local Autonomous AI Assistant (Zero API Key Edition)
Supports Text CLI, Autonomous Task Engine, & Continuous Voice Mode!
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from modules.agent_loop import AutonomousAgentLoop
from modules.voice_engine import VoiceEngine

def run_continuous_voice_mode(agent: AutonomousAgentLoop):
    voice = VoiceEngine()
    print("\n🎙️ [CONTINUOUS VOICE MODE STARTED - NIKKI IS LISTENING]")
    print("Say 'exit' or 'stop' to end voice mode.\n")
    voice.speak("Hello! Continuous voice mode is active. I am Nikki, and I am listening.")

    while True:
        try:
            spoken_text = voice.listen(timeout_sec=7)
            if not spoken_text or "Notice" in spoken_text:
                continue

            if spoken_text.lower() in ["exit", "stop", "quit"]:
                voice.speak("Goodbye! Voice mode deactivated.")
                print("Exiting voice mode.")
                break

            print(f"\n🗣️ You Said: {spoken_text}")
            result = agent.run_task(spoken_text)

            # Speak response out loud
            if result and isinstance(result, str):
                # Clean markdown tags for TTS speaking
                clean_result = result.replace("*", "").replace("#", "").replace("`", "")[:250]
                voice.speak(clean_result)
        except (KeyboardInterrupt, EOFError):
            break

def main():
    print("=" * 65)
    print(" 🌸 NIKKI - YOUR AUTONOMOUS LOCAL AI ASSISTANT 🌸 ")
    print("=" * 65)
    print("Capabilities: Web Search, File Operations, Command Execution,")
    print("WhatsApp, Instagram, SMS, Phone Calling, Android Control,")
    print("IP Camera Streams, Voice Listening/Speaking & Visual Web Face GUI!")
    print("=" * 65)

    agent = AutonomousAgentLoop(model_name="llama3.2")

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--voice", "-v", "voice"]:
            run_continuous_voice_mode(agent)
        elif arg in ["--gui", "-g", "gui", "face"]:
            from modules.web_gui_server import start_gui_server
            start_gui_server()
        else:
            user_task = " ".join(sys.argv[1:])
            agent.run_task(user_task)
    else:
        print("\nCommands:")
        print(" - Type any task to run")
        print(" - Type 'voice' to start continuous Voice Conversation Mode")
        print(" - Type 'gui' or 'face' to open Nikki's Visual Web Face Dashboard")
        print(" - Type 'exit' to quit")
        while True:
            try:
                user_task = input("\nYou > ").strip()
                if user_task.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break
                elif user_task.lower() == "voice":
                    run_continuous_voice_mode(agent)
                elif user_task.lower() in ["gui", "face"]:
                    from modules.web_gui_server import start_gui_server
                    start_gui_server()
                elif user_task:
                    agent.run_task(user_task)
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    main()
