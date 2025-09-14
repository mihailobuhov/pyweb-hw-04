import socket

def run_client():
    host = socket.gethostname()
    port = 5000

    socket_client = socket.socket()
    socket_client.connect((host, port))
    message = input('>>> ')

    while message.lower().strip() != 'quit':
        socket_client.send(message.encode())
        msg = socket_client.recv(1024).decode()
        print(f'Received message: {msg}')
        message = input('>>> ')

    socket_client.close()

if __name__ == '__main__':
    run_client()
