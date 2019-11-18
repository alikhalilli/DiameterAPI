import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_sock.connect(('127.0.0.1', 6666))

count = 0
while True:
    count += 1
    print(f'input {count}')
    data = input()
    print(data)
    print(client_sock)
    client_sock.sendall(data.encode('utf-8'))
    d = client_sock.recv(1024)
    if d != b'':
        print(d)
