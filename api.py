import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

log_file_name = f"/home/logs/api_{time.strftime('%Y%m%d_%H%M%S')}.log"
os.makedirs(os.path.dirname(log_file_name), exist_ok=True)

logging.basicConfig(
    filename=log_file_name,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info("Received request")
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Hello, World!")

def run(server_class=HTTPServer, handler_class=HelloHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting server on :{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Stopping server")

if __name__ == "__main__":
    run()
