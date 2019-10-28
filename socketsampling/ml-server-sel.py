import select
import socket
import queue


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server_address = ('localhost', 1234)
print('Starting up on {} port {}'.format(*server_address), file=sys.stderr)
server.bind(server_address)
server.listen()

# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []
message_queues = {}

while inputs:
    readable, writable, exceptional = select.select(inputs,
                                                    outputs,
                                                    inputs)
    
