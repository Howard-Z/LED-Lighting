import http.server
import socketserver
import json

# Define the port you want to run the server on
PORT = 8000

# Create a custom handler to serve the requests
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            # Attempt to parse the incoming JSON data
            json_data = json.loads(post_data.decode('utf-8'))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # You can process the JSON data here
            # For this example, we'll just echo it back
            response_data = json.dumps(json_data)
            self.wfile.write(response_data.encode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Invalid JSON data')
        

# Create the server and bind it to the specified port
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}")
    
    # Start the server and keep it running until interrupted (e.g., Ctrl+C)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")