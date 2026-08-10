#!/usr/bin/env bash
clear
echo "========================================================================="
echo " 🌸 NIKKI - YOUR AUTONOMOUS LOCAL AI ASSISTANT (ONE-CLICK LAUNCHER) 🌸"
echo "========================================================================="
echo ""
echo "Select how you want to launch Nikki:"
echo ""
echo "  [1] Launch Nikki Continuous Voice Mode (--voice)"
echo "  [2] Launch Nikki Visual Web Face Dashboard (--gui)"
echo "  [3] Run System Health & Security Diagnostic Audit"
echo "  [4] Start Interactive Terminal CLI Mode"
echo "  [5] Exit"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
  1)
    echo "Launching Nikki Continuous Voice Mode..."
    python main.py --voice
    ;;
  2)
    echo "Launching Nikki Visual Web Face Dashboard..."
    python main.py --gui
    ;;
  3)
    echo "Running System Diagnostic..."
    python -c "from modules.health_checker import SystemHealthChecker; SystemHealthChecker().run_full_diagnostic()"
    ;;
  4)
    python main.py
    ;;
  5)
    exit 0
    ;;
  *)
    echo "Invalid choice."
    ;;
esac
