import socket
import selectors
import types

host = '127.0.0.1'
port = 1234

sel = selectors.DefaultSelector()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f'Listening on, {(host, port)}')
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f'Accepted connection from {addr}')
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
