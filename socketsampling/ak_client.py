import socket

server_addr = ('localhost', 6666)

with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as client_sock:
    client_sock.connect(server_addr)
    print(f'Client sock: {client_sock}')
    message = 'This is the message. It will be repeated'.encode('utf-8')
    client_sock.sendall(message)
    received_amount = 0
    total_bytes = len(message)
    from_server = client_sock.recv(16)
    print(from_server.decode('utf-8'))
    while received_amount < total_bytes:
        received_amount += len(from_server)
