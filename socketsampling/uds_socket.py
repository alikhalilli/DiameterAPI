import socket
import sys
import os

server_address = './uds_socket'

try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the address
print('Starting up on {}'.format(server_address))
sock.bind(server_address)
sock.listen(1)

while True:
    print('Waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('Connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('Received {!r}'.format(data))
            if data:
                print('Sending data back to the client')
                connection.sendall(data)
            else:
                print('No data from', client_address)
                break
    finally:
        connection.close()
        
