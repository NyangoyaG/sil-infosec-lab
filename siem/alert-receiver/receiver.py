from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime, timezone


class AlertReceiver(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/alerts":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        print(
            f"\n[{datetime.now(timezone.utc).isoformat()}] "
            f"ALERT RECEIVED:\n{json.dumps(payload, indent=2)}",
            flush=True,
        )

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Alert received")

    def log_message(self, format, *args):
        print(f"[HTTP] {format % args}", flush=True)


server = HTTPServer(("0.0.0.0", 8080), AlertReceiver)
print("SIEM alert receiver listening on port 8080", flush=True)
server.serve_forever()
