import socket

server_address = ('localhost', 6666)
"""
socket() -> bind() -> listen() -> accept() -> read() -> write() -> read() -> close()
"""

with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as server_sock:
    server_sock.bind(server_address)
    server_sock.listen()
    client_sock, addr = server_sock.accept()
    with client_sock:
        print(f'Connected by addr:{addr}')
        print(f'Client socket: {client_sock}')
        print(f'Server socket: {server_sock}')
        print(f'Peername: {client_sock.getpeername()}')
        while True:
            data = client_sock.recv(16)
            if data:
                print(f'Data: {data}')
                client_sock.sendall(data)
            else:
                print(f'No data from {addr}')
                break
