import binascii
import socket
import struct
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

values = (1, b'ab', 2.7)
packer = struct.Struct('I2sf')
packed_data = packer.pack(*values)
print(f'values={values}')

try:
    print(f'Sending {binascii.hexlify(packed_data)}')
    sock.sendall(packed_data)
finally:
    print('Closing socket')
    sock.close()
