from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Define the server's IP address and port
IP_ADDRESS = '127.0.0.1'
PORT = 7070

class MainServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {
            'message': 'Hello from the main server!'
        }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        data_length = int(self.headers['Content-Length'])
        data = self.rfile.read(data_length).decode()
        print(f"Received POST data: {data}")
        print(f"Main Server Welcomes you")
        
        self.send_response(201, "Created")
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("POST request received!\n".encode())
        self.wfile.write("Welcome from the main server".encode())

def run_main_server():
    server_address = (IP_ADDRESS, PORT)
    httpd = HTTPServer(server_address, MainServerHandler)
    print(f'Starting main server on {IP_ADDRESS}:{PORT}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_main_server()
