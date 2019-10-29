import binascii
import socket
import struct
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)

unpacker = struct.Struct('I2sf')

while True:
    print('\nWaiting for a connection')
    connection, client_address = sock.accept()
    try:
        data = connection.recv(unpacker.size)
        print('Received {!r}'.format(binascii.hexlify(data)))
        unpacked_data = unpacker.unpack(data)
        print(f'unpacked: {unpacked_data}')
    finally:
        connection.close()
