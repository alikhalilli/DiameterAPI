import socket


class FixedLengthSocket:
    def __init__(self, message_len, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
        else:
            self.sock = sock
        self.message_len = message_len

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        total_sent = 0
        while total_sent < self.message_len:
            sent = self.sock.send(msg[total_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent += sent

    def receive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < self.message_len:
            chunk = self.sock.recv(min(self.message_len - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)
