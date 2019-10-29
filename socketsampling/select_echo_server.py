import select
import socket
import sys
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

server_address = ('localhost', 10000)
print('Starting up on {} port {}'.format(*server_address))
server.bind(server_address)
server.listen(5)

inputs = [server]
outputs = []

message_queues = {}


while inputs:
    print('Waiting for the next event')
    readable, writable, exceptional = select.select(inputs,
                                                    outputs,
                                                    inputs)
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            print(f'Connection from {client_address}')
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print(f'{data} received from {s.getpeername()}')
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]
