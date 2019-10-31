import socket
import select


class NetworkHandler:
    def __init__(self, host, port, sockfamily=socket.AF_INET, socktype=socket.SOCK_STREAM):
        self._host = host
        self._port = port
        self._addr = (host, port)
        self._family = sockfamily
        self._type = socktype
        self._prepare_socket()

    @property
    def serversocket(self):
        return self._server_socket

    def _prepare_socket(self):
        self._server_socket = socket.socket(self._family, self._type)
        self._server_socket.bind(self._addr)
        self._server_socket.listen()

    def reset_socket(self):
        pass

    def accept_wrapper(self):
        pass

    def process_request(self):
        pass


nh = NetworkHandler(host='localhost', port=6666)
with nh.serversocket as serversock:
    client_sock, client_addr = serversock.accept()
