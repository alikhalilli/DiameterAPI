import socket

server_address = ('localhost', 6666)
server_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
msg_len = len('This is the message. It will be repeated')
with server_socket:
    server_socket.bind(server_address)
    server_socket.listen()
    client_socket, client_addr = server_socket.accept()
    with client_socket:
        while True:
            data = client_socket.recv(16)
            print(data)
            if data == b'':
                break
