import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print('Connection to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    message = 'This is the message. It will be repeated'.encode('utf-8')
    print('Sending {!r}'.format(message))
    sock.sendall(message)
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('Received {!r}'.format(data))
finally:
    print('Closing socket')
    sock.close()
