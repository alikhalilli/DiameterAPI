import socket

server_addr = ('10.1.0.12', 6666)
client_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

client_sock.bind(('', 6666))

with client_sock:
    client_sock.connect(server_addr)
    print(f'Client sock: {client_sock}')
    message = b'salamsalamsalamThis is the message. It will be repeated'
    sent_amount = 0
    i = 0
    client_sock.sendall(message)
    print(client_sock.recv(1024))
