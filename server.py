import http.server
import socketserver
import base64

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Mediapipe Nexus"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Nexus"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        auth = self.headers.get('Authorization')
        if auth is None:
            self.do_AUTHHEAD()
            self.wfile.write('Authentification requise'.encode('utf-8'))
            return
        if auth == 'Basic ' + base64.b64encode(b'admin:Jaajpmds1f$').decode():
            http.server.SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_AUTHHEAD()
            self.wfile.write('Authentification échouée'.encode('utf-8'))
            return

if __name__ == '__main__':
    with socketserver.TCPServer(("", 8000), AuthHandler) as httpd:
        print("Serveur en cours d'exécution sur le port 8000")
        httpd.serve_forever()