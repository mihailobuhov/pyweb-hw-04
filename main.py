import mimetypes
import json
import logging
import socket
import urllib.parse
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

BASE_DIR = Path()
BUFFER_SIZE = 1024
HTTP_PORT = 3000
HTTP_HOST = '0.0.0.0'
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 5000

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        print(route.query)
        match route.path:
            case '/':
                self.send_html('index.html')
            case '/message':
                self.send_html('message.html')
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html('error.html', 404)
        
    def do_POST(self):
        size = self.headers.get('Content-Length')
        data = self.rfile.read(int(size))
        # print(data)
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_client.sendto(data, (SOCKET_HOST, SOCKET_PORT))
        socket_client.close()

        self.send_response(302)
        self.send_header('Location', '/message')
        self.end_headers()

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-Type', mime_type)
        else:
            self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

def save_data_from_form(data):
        parse_data = urllib.parse.unquote_plus(data.decode())
        try:
            # Розпарсити дані з форми
            parse_dict = {key: value.strip() for key, value in [el.split('=') for el in parse_data.split('&')]}

            # Взяти поточний час як ключ
            timestamp = datetime.now().isoformat()

            # Прочитати існуючий файл, якщо він існує
            storage_file = Path('storage/data.json')
            if storage_file.exists():
                with open(storage_file, 'r', encoding='utf-8') as file:
                    data_store = json.load(file)
            else:
                data_store = {}

            # Додати нові дані з поточним часом як ключем 
            data_store[timestamp] = parse_dict

            # Записати оновлені дані в файл 
            with open(storage_file, 'w', encoding='utf-8') as file:
                json.dump(data_store, file, ensure_ascii=False, indent=4)
        except ValueError as err:
            logging.error(err)
        except OSError as err: 
            logging.error(err)


def run_socket_server(host, port):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_server.bind((host, port))
    logging.info("Starting socket server")
    try:
        while True:
            msg, address = socket_server.recvfrom(BUFFER_SIZE)
            logging.info(f"Socket received {address}: {msg}")
            save_data_from_form(msg)
    except KeyboardInterrupt:
        pass
    finally:
        socket_server.close()


def run_http_server(host, port):
    address = (host, port)
    http_server = HTTPServer(address, HttpHandler)
    logging.info("Starting http server")
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        http_server.server_close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    http_server = Thread(target=run_http_server, args=(HTTP_HOST, HTTP_PORT))
    http_server.start()

    socket_server = Thread(target=run_socket_server, args=(SOCKET_HOST, SOCKET_PORT))
    socket_server.start()