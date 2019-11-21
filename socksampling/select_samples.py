import select
import socket
import selectors
from collections import namedtuple
from abc import ABCMeta, abstractmethod, Mapping

EVENT_READ = (1 << 0)
EVENT_WRITE = (1 << 1)

SelectorKey = namedtuple('SelectorKey', ['sock', 'fd', 'events', 'data'])


class SocketSelectorMapping(Mapping):
    def __init__(self, selector):
        self._selector = selector

    def __len__(self):
        return len(self._selector._fd_to_selkey_dict)


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
        self._sock_to_key = {}
        self._readers = set()
        self._writers = set()
        self._select = select

    def register(self, sock, events, data=None):
        key = SelectorKey(sock, sock._get_fd(), events, data)

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
            key = self._sock_to_key.pop(sock._get_fd())
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
                self._readers, self._writers, [], timeout=timeout)
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


class Server:
    def __init__(self, host, port, sock):
        self._host = host
        self._port = port
        self._socket = sock

    def prepare(self):
        self.sock.bind((self._host, self._port))
        self.sock.listen(100)

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


"""mysock = MySocket()

print(mysock.get_file_descriptor())
"""

person = namedtuple('Person', ['name', 'age', 'sex'])

ali = person(name='Ali', age=25, sex='male')

print(ali.name)
