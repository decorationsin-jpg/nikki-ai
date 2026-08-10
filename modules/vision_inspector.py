"""
Nikki Computer Vision & Screen / Webcam Inspector Engine.
Captures PC screen screenshots or webcam snapshots and analyzes visual content locally.
"""
import subprocess
from pathlib import Path

class VisionInspector:
    """
    Local Computer Vision & Screen/Webcam Inspector.
    """

    def capture_pc_screen(self, save_path: str = "pc_screen.png") -> str:
        """Captures a full screenshot of your PC desktop."""
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            out_path = Path(save_path)
            screenshot.save(out_path)
            return f"🖥️ PC Screen Screenshot captured and saved to: {out_path.resolve()}"
        except ImportError:
            # Fallback using PowerShell
            cmd = f'powershell "Add-Type -AssemblyName System.Windows.Forms; $b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height; $g = [System.Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size); $bmp.Save(\'{save_path}\')"'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return f"🖥️ Screen captured via Windows PowerShell to: {save_path}" if res.returncode == 0 else str(res.stderr)

    def capture_webcam_photo(self, save_path: str = "webcam_photo.jpg") -> str:
        """Captures a snapshot from your PC's webcam."""
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(save_path, frame)
                cap.release()
                return f"📷 Webcam snapshot captured successfully to: {save_path}"
            cap.release()
            return "Failed to read frame from webcam."
        except ImportError:
            return "OpenCV not installed yet. Install via `pip install opencv-python pillow` for full webcam support."
        except Exception as e:
            return f"Webcam capture error: {str(e)}"
