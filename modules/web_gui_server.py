"""
Lightweight Web Server for Nikki's Face Avatar & GUI Dashboard.
Hosts Nikki's visual interface on local port 5000 so you can open her face and chat via browser.
"""
import http.server
import socketserver
import json
import urllib.parse
from pathlib import Path
from modules.agent_loop import AutonomousAgentLoop

PORT = 5000
WEB_DIR = Path(__file__).parent.parent / "web_gui"
agent = AutonomousAgentLoop(model_name="llama3.2")

class NikkiGUIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR.resolve()), **kwargs)

    def do_POST(self):
        """API Endpoint for user tasks submitted from Nikki's Web GUI Face Dashboard."""
        if self.path == "/api/task":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                user_goal = data.get("goal", "")
                result = agent.run_task(user_goal)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response_payload = json.dumps({"status": "success", "response": str(result)})
                self.wfile.write(response_payload.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_error(404)

def start_gui_server():
    """Starts Nikki's Web GUI Server on localhost:5000."""
    with socketserver.TCPServer(("", PORT), NikkiGUIHandler) as httpd:
        print(f"🌸 [Nikki Visual Face Dashboard]: Live at http://localhost:{PORT}")
        print("Open http://localhost:5000 in your browser to see Nikki's face and chat with her!")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Nikki GUI server.")

if __name__ == "__main__":
    start_gui_server()
