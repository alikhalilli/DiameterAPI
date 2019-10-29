import selectors
import socket

mysel = selectors.DefaultSelector()
keep_running = True


def read(connection, mask):
    global keep_running
    client_address = connection.getpeername()
    print(f'Read {client_address}')
    data = connection.recv(1024)
    if data:
        print(f'{data} received')
        connection.sendall(data)
    else:
        print(' closing')
        mysel.unregister(connection)
        connection.close()
        keep_running = False


def accept(sock, mask):
    new_connection, addr = sock.accept()
    print(f'Accept {addr}')
    new_connection.setblocking(False)
    mysel.register(new_connection, selectors.EVENT_READ, read)


server_address = ('localhost', 10000)
print('Starting up on {} port {}'.format(*server_address))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(server_address)
server.listen(5)
mysel.register(server, selectors.EVENT_READ, accept)

while keep_running:
    print('Waiting for I/O')
    for key, mask in mysel.select(timeout=1):
        callback_func = key.data
        callback_func(key.fileobj, mask)

print('Shutting down')
mysel.close()
