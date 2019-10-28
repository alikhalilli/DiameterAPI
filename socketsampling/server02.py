import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)

while True:
    print('Waiting for a connection')
    connection, client_address = sock.accept()
    print(connection, client_address)
    try:
        print('Connection from', client_address)
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no data from ', client_address)
                break
    finally:
        connection.close()
