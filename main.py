import socket
from views import *
URLS = {
    '/': index,
    '/blog': blog
}

def parse_req(request):
    parsed = request.split(' ')
    if len(parsed) < 2:
        return (None, None)
    method = parsed[0]
    url = parsed[1]
    return (method, url)

def generate_headers(method, url):
    if not method == "GET":
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)
    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)
    else:
        return ('HTTP/1.1 200 OK\n\n', 200)

def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return URLS[url]()

def generate_response(request):
    method, url = parse_req(request)
    if method is None or url is None:
        return ('HTTP/1.1 400 Bad Request\n\nBad Request').encode()
    headers, code = generate_headers(method, url)
    body = generate_content(code,url)

    return (headers + body).encode()

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()
    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        print(request.decode('utf-8'))
        print()
        print(addr)

        response = generate_response(request.decode('utf-8'))
        client_socket.sendall(response)
        client_socket.close()

if __name__ == '__main__':
    run()
