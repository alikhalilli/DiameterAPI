import asyncio
import selectors
import socket

sel = selectors.DefaultSelector()


def acceptor(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, handler)


def handler(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        data = "ali".encode() + data
        conn.sendall(data)  # Hope it won't block


sock = socket.socket()
sock.bind(('localhost', 8899))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, acceptor)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
