import socket
import selectors
import types

messages = [
    b'Message 1 from client',
    b'Message 2 from client'
]


def start_connections(host, port, n_conn):
    server_addr = (host, port)
    for i in range(n_conn):
        connid = i+1
        print(f'Starting connection {connid} to {server_addr}')
        client_sock = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
        client_sock.setblocking(0)
        client_sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=sum((len(m) for m in messages)),
                                     recv_total=0,
                                     messages=list(messages),
                                     outb=b'')


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
