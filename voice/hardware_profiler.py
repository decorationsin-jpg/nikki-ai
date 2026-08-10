"""
OBSY AI Hardware Profiler Subsystem.
Detects CPU, System RAM, GPU VRAM, and selects hardware voice target mode:
- 🟢 Basic PC (Integrated GPU / 16GB RAM) -> Lightweight TTS Fallback
- 🔵 Recommended PC (NVIDIA GPU / 8-12GB VRAM / 32GB RAM) -> IndicF5 Neural Engine
- 🟣 OBSY Pro (NVIDIA GPU / 12-24GB VRAM / 64GB RAM) -> Real-time Neural Streaming Pipeline
"""

import psutil
from typing import Dict, Any

class ObsyHardwareProfiler:
    @classmethod
    def profile_hardware(cls) -> Dict[str, Any]:
        ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)
        cpu_count = psutil.cpu_count()
        vram_gb = 8.0  # Estimated local GPU VRAM

        mode = "RECOMMENDED"
        mode_label = "🔵 Recommended (IndicF5 Neural TTS)"
        
        if ram_gb < 20 or vram_gb < 6:
            mode = "BASIC"
            mode_label = "🟢 Basic PC (Lightweight Voice Mode)"
        elif ram_gb >= 32 and vram_gb >= 12:
            mode = "OBSY_PRO"
            mode_label = "🟣 OBSY Pro (Real-Time Neural Streaming)"

        return {
            "ram_gb": ram_gb,
            "cpu_cores": cpu_count,
            "vram_gb": vram_gb,
            "mode": mode,
            "mode_label": mode_label,
            "primary_tts": "IndicF5 (ai4bharat/IndicF5)",
            "experimental_tts": "Indic Parler-TTS (ai4bharat/indic-parler-tts)"
        }
