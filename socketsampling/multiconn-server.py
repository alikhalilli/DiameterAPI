import selectors
import socket

sel = selectors.DefaultSelector()


def accept(sock, mask):
    conn, addr = sock.accept()
    print(f"Accepted conn: {conn} from addr: {addr}\n")
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print(f"Echoing {data} to {conn}\n")
        conn.send(data)
    else:
        print(f"Closing {conn}\n")
        sel.unregister(conn)
        conn.close()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 1234))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    print(f"Events: {events}\n")
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)


