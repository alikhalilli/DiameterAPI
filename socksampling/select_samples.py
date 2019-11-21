import select
import socket
from collections import namedtuple
from abc import ABCMeta, abstractmethod
from collections.abc import Mapping

EVENT_READ = (1 << 0)
EVENT_WRITE = (1 << 1)

SelectorKey = namedtuple('SelectorKey', ['sock', 'fd', 'events', 'clb'])


def _get_fd(socket):
    if isinstance(socket, int):
        return socket
    try:
        fd = int(socket.fileno())
    except (AttributeError, TypeError, ValueError):
        raise ValueError(f"Invalid socket obj: {socket}")
    if fd < 0:
        raise ValueError("Invalid file descriptor: {fd}")
    return fd


class SocketSelectorMap(Mapping):
    def __init__(self, socket_selector):
        self._selector = socket_selector

    def __len__(self):
        return len(self._selector._fd_to_selkey_dict)

    def __getitem__(self, sock):
        try:
            fd = self._selector._sock_to_fd(sock)
            return self._selector._fd_to_selkey_dict[fd]
        except KeyError:
            raise KeyError(f"{sock} is not refistered.")

    def __iter__(self):
        return next(self._selector._fd_to_selkey_dict)


class BaseSockSelector(metaclass=ABCMeta):
    @abstractmethod
    def register(self, sock, events, data=None):
        raise NotImplementedError

    @abstractmethod
    def unregister(self, sock):
        raise NotImplementedError

    @abstractmethod
    def modify(self, sock, events, data=None):
        self.unregister(sock)
        self.register(sock, events, data)

    @abstractmethod
    def select(self, timeout=None):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def get_map(self):
        raise NotImplementedError

    @abstractmethod
    def get_key(self, sock):
        mapping = self.get_map()
        if mapping is None:
            raise RuntimeError('Selector is closed')
        try:
            return mapping[sock]
        except KeyError:
            raise KeyError("{!r} is not registered".format(sock)) from None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class SocketSelector(BaseSockSelector):
    def __init__(self):
        super().__init__()
        self._sock_to_key = {}
        self._map = SocketSelectorMap(self)
        self._select = select
        self._readers = set()
        self._writers = set()

    def get_key(self):
        pass

    def modify(self, sock):
        pass

    def _sock_to_fd(self, sock):
        return _get_fd(sock)

    def register(self, sock, events, data=None):
        key = SelectorKey(sock, _get_fd(sock), events, data)

        if key.fd in self._sock_to_key:
            raise KeyError(
                "Socket: {socket} with {key.fd} is already registered")
        self._sock_to_key[key.fd] = key

        if events & EVENT_READ:
            self._readers.add(key.fd)
        elif events & EVENT_WRITE:
            self._writers.add(key.fd)
        return key

    def unregister(self, sock):
        try:
            key = self._sock_to_key.pop(_get_fd(sock))
        except KeyError:
            raise KeyError(f"{sock} is not registered")
        self._writers.discard(key.fd)
        self._readers.discard(key.fd)
        return key

    def select(self, timeout=None):
        timeout = None if timeout is None else max(timeout, 0)
        ready = []
        try:
            r, w, _ = self._select.select(
                self._readers, self._writers, [], timeout)
        except InterruptedError:
            return ready
        r = set(r)
        w = set(w)

        for sock in r | w:
            events = 0
            if sock in r:
                events = events | EVENT_READ
            if sock in w:
                events = events | EVENT_WRITE
            key = self._sock_to_key[sock]
            if key:
                ready.append((key, events & key.events))
        return ready

    def close(self, s):
        self._sock_to_key.clear()
        self._map = None

    def get_map(self):
        return self._map


class Server:
    def __init__(self, host, port, sock):
        self._host = host
        self._port = port
        self._socket = sock

    def prepare(self):
        self.sock.bind((self._host, self._port))
        self.sock.listen(100)

    def accept(self):
        return self.sock.accept()

    def __enter__(self):
        return self.sock

    def __exit(self, *args):
        self.sock.close()

    @property
    def sock(self):
        return self._socket.socket

    @sock.setter
    def sock(self, val):
        self._socket = val

    def __repr__(self):
        return f"""Host: {self._host}
        Port: {self._port}
        Socket: {self._socket}
        """


class MySocket:
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, blocking=True):
        self._socket = socket.socket(family=family, type=type)
        self._socket.setblocking(blocking)

    @property
    def socket(self):
        return self._socket

    def _get_fd(self):
        if isinstance(self._socket, int):
            return self._socket
        try:
            fd = int(self._socket.fileno())
        except (AttributeError, TypeError, ValueError):
            raise ValueError(f"Invalid socket obj: {self._socket}")
        if fd < 0:
            raise ValueError("Invalid file descriptor: {fd}")
        return fd

    def get_file_descriptor(self):
        return self._get_fd()

    @socket.setter
    def socket(self, val):
        self._socket = socket

    def __repr__(self):
        return f"{self._socket}"


server = Server(host='127.0.0.1',
                port=6666,
                sock=MySocket(blocking=False))

server.prepare()

sockselector = SocketSelector()


def acceptor(sock, mask):
    cli_sock, addr = sock.accept()
    cli_sock.setblocking(False)
    sockselector.register(cli_sock, EVENT_READ, handler)


def handler(cli_sock, mask):
    cli_address = cli_sock.getpeername()
    total_bytes = 0
    data = cli_sock.recv(1024)
    total_bytes += len(data)
    if data != b'':
        print(f"{data} from {cli_address}, total bytes: {total_bytes}")
    else:
        sockselector.unregister(cli_sock)
        cli_sock.close()


sockselector.register(server.sock, EVENT_READ, acceptor)
while True:
    for key, mask in sockselector.select(timeout=1):
        clb_func = key.clb
        clb_func(key.sock, mask)
