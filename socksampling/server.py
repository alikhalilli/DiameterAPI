import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.bind(('127.0.0.1', 6666))
server_sock.listen(100)

client_sock, client_addr = server_sock.accept()
print(client_sock, client_addr)

while True:
    data = client_sock.recv(1024)
    print(client_sock)
    if data != b'':
        print(data)
