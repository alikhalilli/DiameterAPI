import socket

server_address = ('localhost', 6666)
server_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
msg_len = len('This is the message. It will be repeated')
# server_socket.setblocking(0)
# server_socket.settimeout(10)
with server_socket:
    server_socket.bind(server_address)
    server_socket.listen()
    client_socket, client_addr = server_socket.accept()
    print(f"socket: {client_socket} \n addr:{client_addr}")
    with client_socket:
        while True:
            data = client_socket.recv(16)
            client_socket.sendall(data)
            print(data)
            if data == b'':
                break
