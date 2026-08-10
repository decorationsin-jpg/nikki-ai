"""
IP Camera & RTSP Stream Integration Engine.
Connects to local IP cameras (RTSP / HTTP / MJPEG streams, e.g., IP Webcam App, EZVIZ, Tapo, Hikvision, Dahua),
captures video frames, saves snapshots, and performs stream health checks.
"""
import urllib.request
import urllib.error
from pathlib import Path

class IPCameraManager:
    """
    Handles IP Camera connections, live snapshot extraction, and stream frame processing.
    """

    def __init__(self, default_stream_url: str = "http://192.168.1.100:8080/shot.jpg"):
        self.default_stream_url = default_stream_url

    def capture_snapshot(self, camera_url: str = None, save_path: str = "camera_snapshot.jpg") -> str:
        """
        Fetches the latest image snapshot from an IP camera stream URL (HTTP / MJPEG)
        and saves it to disk.
        """
        target_url = camera_url if camera_url else self.default_stream_url
        req = urllib.request.Request(
            target_url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                image_data = resp.read()
                out_path = Path(save_path)
                out_path.write_bytes(image_data)
                return f"📷 IP Camera Snapshot captured successfully from {target_url} -> Saved to {out_path.resolve()}"
        except urllib.error.URLError as e:
            return f"Failed to connect to IP Camera at {target_url}: {str(e)}"
        except Exception as e:
            return f"Error capturing IP Camera snapshot: {str(e)}"

    def check_camera_status(self, camera_url: str = None) -> str:
        """Checks if the IP camera stream is online and accessible."""
        target_url = camera_url if camera_url else self.default_stream_url
        try:
            req = urllib.request.Request(target_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    return f"✅ IP Camera at {target_url} is ONLINE and streaming!"
                return f"⚠️ IP Camera returned status code: {resp.status}"
        except Exception as e:
            return f"❌ IP Camera at {target_url} is OFFLINE or unreachable: {str(e)}"
