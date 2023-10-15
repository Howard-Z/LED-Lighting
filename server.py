import http.server
import json
import _thread as thread
from room import Room


class JSONRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can perform any setup or initialization here

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def parse_eff(self, json_data):
        global room
        room.dev_list[json_data["dev"] - 1].add_eff(json_data["eff_id"], json_data["params"])

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            json_data = json.loads(post_data)
            self.parse_eff(json_data)
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON data"}).encode('utf-8'))
            return

        # Handle the JSON data as needed
        # In this example, we just send it back as a response
        self._set_headers()
        self.wfile.write(json.dumps(json_data).encode('utf-8'))

def run(server_class=http.server.HTTPServer, handler_class=JSONRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()


thread.start_new_thread(run, ())
print("called init")  
room = Room()
room.add_dev("192.168.1.121", 329)
room.add_dev("192.168.1.134", 300)
room.add_dev("192.168.1.123", 329)
room.add_dev("192.168.1.127", 329)
room.add_dev("192.168.1.139", 256)
print("added devices ")
room.run()