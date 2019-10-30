import socket

server_addr = ('localhost', 6666)

with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as client_sock:
    client_sock.connect(server_addr)
    print(f'Client sock: {client_sock}')
    message = 'This is the message. It will be repeated'.encode('utf-8')
    sent_amount = 0
    i = 0
    client_sock.sendall(message)
