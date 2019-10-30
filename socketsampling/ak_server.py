import socket
import selectors
import types

sel = selectors.DefaultSelector()
server_address = ('localhost', 6666)
server_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
msg_len = len('This is the message. It will be repeated')
# server_socket.setblocking(0)
# server_socket.settimeout(10)
sel.register(server_socket, selectors.EVENT_READ, data=None)


def accept_wrapper(server_sock):
    client_sock, client_addr = server_sock.accept()
    print(f"Client sock: {client_sock}, addr:{client_addr}")
    client_sock.setblocking(0)
    data = types.SimpleNamespace(addr=client_addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(client_sock, events, data=data)


def service_connection(key, mask):
    client_sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = client_sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f'Closing connection to {data.addr}')
            sel.unregister(client_sock)
            client_sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f'Echoing {data.outb} to {data.addr}')
            sent = client_sock.send(data.outb)
            data.outb = data.outb[sent:]


while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            pass


"""

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
"""
