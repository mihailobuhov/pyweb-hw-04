import socket

def run_server():
    host = socket.gethostname()
    port = 5000

    socket_server = socket.socket()
    socket_server.bind((host, port))
    socket_server.listen()

    conn, address = socket_server.accept()
    print(f'Connected by {address}')

    while True:
        msg = conn.recv(1024).decode()
        if not msg: 
            break
        print(f'Received message: {msg}')
        message = input('>>> ')
        conn.send(message.encode())
    conn.close()
    socket_server.close()

if __name__ == '__main__':
    run_server()
