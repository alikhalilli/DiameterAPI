import socket
import select

select.select

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.bind(('127.0.0.1', 6666))
server_sock.listen(100)

client_sock, client_addr = server_sock.accept()
print(client_sock, client_addr)

while True:
    from_client = client_sock.recv(1024)
    if from_client != b'':
        print(f"from client: {from_client}")
        to_client = input("input:")
        client_sock.send(to_client.encode('utf-8'))
    else:
        client_sock.close()
    print(client_sock)
