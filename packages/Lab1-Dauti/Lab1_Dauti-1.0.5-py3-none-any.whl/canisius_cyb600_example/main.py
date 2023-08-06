import http.server
import socketserver
import datetime


def start_server():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            now = datetime.datetime.now()
            current_time = now.strftime("%I:%M:%S %p")
            self.wfile.write(bytes(f'The time is {current_time}', 'utf-8'))

    port = 8080

    with socketserver.TCPserver(("", port), Handler) as httpd:
        print(f"serving at port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

    print("Server stopped.")
