import http.server as server
import urllib.parse as parse

class GameHTTPRequestHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("Just received a GET request")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        print(parse.parse_qs(parse.urlparse(self.path).query).get("var"))
        self.wfile.write(b'Hello world')

        return

    def log_request(self, code=None, size=None):
        print('Request')

    def log_message(self, format, *args):
        print('Message')


PORT = 34567
handler = GameHTTPRequestHandler

try:
    httpd = server.HTTPServer(("", PORT), handler)
    print('Started http server')
    httpd.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting do wn server')
    httpd.socket.close()
print("WHAT")