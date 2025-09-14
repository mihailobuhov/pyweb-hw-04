import socket # socket_server(UDP)

def run_server():
    host = socket.gethostname()
    port = 5000

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_server.bind((host, port))
    print(f"Starting server at {host}: {port}")

    while True:
        msg, address = socket_server.recvfrom(1024)
        print(f"Received message from {address}: {msg.decode()}")
        responce = input('>>> ')
        socket_server.sendto(responce.encode(), address)

if __name__ == '__main__':
    run_server()
