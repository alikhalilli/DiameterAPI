import socket
import select
import socketserver
import selectors

__all__ = [
    "NetworkHandler"
]


class NetworkHandler:
    def __init__(self, host, port,
                 sockfamily=socket.AF_INET,
                 socktype=socket.SOCK_STREAM,
                 queue_size=100,
                 activate=False
                 ):
        self._host = host
        self._port = port
        self._addr = (host, port)
        self._family = sockfamily
        self._type = socktype
        self._queue_size = queue_size
        self._activate = activate
        self._prepare_socket()
        self._selector = selectors.SelectSelector()

    @property
    def serversocket(self):
        return self._server_socket

    def _prepare_socket(self, activate=False):
        self._server_socket = socket.socket(self._family, self._type)
        self._server_socket.bind(self._addr)
        self._server_socket.listen(self._queue_size)

    def close_conn(self):
        self.serversocket.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.serversocket.close()


nh = NetworkHandler(host='localhost', port=6666)
with nh:
    nh.server_forever()


class TCPServer:
