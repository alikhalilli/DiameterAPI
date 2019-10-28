import select
import socket
import sys
import queue


# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 10000)
print("Starting up on {} port {}".format(*server_address),
      file=sys.stderr)
server.bind(server_address)
server.listen(5)

# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []

# Outgoing message queues (socket: Queue)
while inputs:
    print('Waiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs,
                                                    outputs, inputs)


message_queues = {}

for s in readable:
    if s is server:
        connection, client_address = s.accept()
        print(f' connection from {client_address}',
              file=sys.stderr)
        connection.setblocking(0)
        inputs.append(connection)
        message_queues[connection] = queue.Queue()
    else:
        data = s.recv(1024)
        if data:
            print("{data} received from {s.getpeername()}",
                  file=sys.stderr)
            message_queues[s].put(data)
            if s not in outputs:
                outputs.append(s)
        else:
            print(f'{client_address} closing', file=sys.stderr)
            if s in outputs:
                outputs.remove(s)
            inputs.remove(s)
            s.close()
            del message_queues[s]

for s in writable:
    try:
        next_msg = message_queues[s].get_nowait()
    except queue.Empty:
        print('  ', s.getpeername(), 'queue empty',
              file=sys.stderr)
        outputs.remove(s)
    else:
        print(f'{next_msg} sending to {s.getpeername}')
        s.send(next_msg)
