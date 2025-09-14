# socket_client.py
import socket

def run_client():
    host = socket.gethostname()
    port = 5000

    socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = input('>>> ')

    while message.lower().strip() != 'quit':
        socket_client.sendto(message.encode(), (host, port))
        msg, server = socket_client.recvfrom(1024)
        print(f"Response message from {server}: {msg.decode()}")
        message = input('>>> ')

    socket_client.close()

if __name__ == '__main__':
    run_client()
