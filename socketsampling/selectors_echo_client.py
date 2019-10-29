import selectors
import socket

mysel = selectors.DefaultSelector()
keep_running = True
outgoing = [
    b'It will be repeated.',
    b'This is the message'
]
bytes_sent = 0
bytes_received = 0

server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
sock.setblocking(False)


mysel.register(
    sock,
    selectors.EVENT_READ | selectors.EVENT_WRITE
)


while keep_running:
    print('Waiting for IO')
    for key, mask in mysel.select(timeout=1):
        connection = key.fileobj
        client_address = connection.getpeername()
        print(f'Client {client_address}')

        if mask & selectors.EVENT_READ:
            print('Ready to read')
            data = connection.recv(1024)
            if data:
                print(f'{data} received')
                bytes_received += len(data)

            keep_running = not(
                data or
                (bytes_received and
                 (bytes_received == bytes_sent))
            )

        if mask & selectors.EVENT_WRITE:
            print('Ready to write')
            if not outgoing:
                print(' switching to read-only')
                mysel.modify(sock, selectors.EVENT_READ)
            else:
                next_msg = outgoing.pop()
                print(f'sending {next_msg}')
                sock.sendall(next_msg)
                bytes_sent += len(next_msg)


print('Shutting down')
mysel.unregister(connection)
connection.close()
mysel.close()
