import http.server
from slack import SlackRequestHandler

def run_server():
    server_address = ('', 8000)  # Change port if needed
    httpd = http.server.HTTPServer(server_address, SlackRequestHandler)
    print('Starting server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
