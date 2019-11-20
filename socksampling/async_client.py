import socket
import asyncio

client_socks = [socket.socket(
    socket.AF_INET, socket.SOCK_STREAM) for _ in range(10)]

[client_sock.connect(('127.0.0.1', 8888)) for client_sock in client_socks]

count = 0
while True:
    count += 1
    data = input("input:")
    for client_sock in client_socks:
        client_sock.sendall(data.encode('utf-8'))
        from_server = client_sock.recv(1024)
        if from_server != b'':
            print(f"from server: {from_server}")
