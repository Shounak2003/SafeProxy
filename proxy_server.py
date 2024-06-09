from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import http.client

# Define the server's IP address and port
PROXY_ADDRESS = '127.0.0.1'
PROXY_PORT = 8080

# Define the main server's address (replace with your main server details)
MAIN_SERVER_ADDRESS = '127.0.0.1'
MAIN_SERVER_PORT = 7070

class ProxyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("Received POST request")
        data_length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(data_length) if data_length > 0 else b''

        if b"Shounak" in data:
            print("Request contains 'Shounak'")
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("Contains Shounak!".encode())
            return
        
        print("Request does not contain 'Shounak'. Prompting for authentication.")
        auth_header = self.headers.get('Authorization')
        if auth_header:
            print("Authorization header:", auth_header)
            auth_info = base64.b64decode(auth_header.split()[1]).decode()
            username, password = auth_info.split(':')

            if password == "12345678":
                print("Authentication successful. Forwarding request to main server.")
                self.forward_request("POST", self.path, self.headers, data)
                return
            else:
                print("Authentication failed. Sending 401 Unauthorized response.")
                self.send_response(401)
                self.send_header('WWW-Authenticate', 'Basic realm="Please enter your credentials."')
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write("Authentication failed".encode())
                return
        else:
            print("No authorization header found. Prompting for authentication.")
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Please enter your credentials."')
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("Authentication required".encode())
            return

    def forward_request(self, method, path, headers, body):
        connection = http.client.HTTPConnection(MAIN_SERVER_ADDRESS, MAIN_SERVER_PORT)
        headers = {key: value for key, value in self.headers.items()}

        if 'Content-Length' in headers:
            headers['Content-Length'] = str(len(body))

        connection.request(method, path, body, headers)
        response = connection.getresponse()

        self.send_response(response.status, response.reason)
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.read())
        connection.close()

def run_proxy_server():
    server_address = (PROXY_ADDRESS, PROXY_PORT)
    httpd = HTTPServer(server_address, ProxyHandler)
    print(f'Starting proxy server on {PROXY_ADDRESS}:{PROXY_PORT}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_proxy_server()
