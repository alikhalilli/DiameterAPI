import time
import queue
import threading
import heapq
from collections import deque
import asyncio


class Awaitable:
    def __await__(self):
        yield self


class ASleep:
    def __await__(self):
        yield time.sleep(2)


def switch():
    return Awaitable()


class Scheduler:
    def __init__(self):
        self.ready = deque()  # functions ready to execute
        self.sleeping = []  # sleeping functions
        self.current = None  # currently executing generator
        self.sequence = 0

    async def sleep(self, delay):
        deadline = time.time() + delay
        self.sequence += 1
        heapq.heappush(self.sleeping, (deadline, self.sequence, self.current))
        self.current = None
        await switch()

    def call_soon(self, func):
        self.ready.append(func)

    def call_later(self, delay, func):
        deadline = time.time() + delay  # expiration time
        # Priority queue
        heapq.heappush(self.sleeping, (deadline, self.sequence, func))

    def run(self):
        while self.ready or self.sleeping:
            if not self.ready:
                # Find the nearest deadline
                deadline, _, func = heapq.heappop(self.sleeping)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready.append(func)
            while self.ready:
                func = self.ready.popleft()
                func()


sched = Scheduler()  # Behind scenes scheduler object


class QueueClosed(Exception):
    pass


class AsyncQueue:
    def __init__(self):
        self.items = deque()
        self.waiting = deque()
        self._closed = False

    def close(self):
        self._closed = True

    def put(self, item):
        if self._closed:
            raise QueueClosed()

        self.items.append(item)
        while self.waiting:
            func = self.waiting.popleft()
            sched.call_soon(lambda: func())

    def get(self, callback):
        if self.items:
            callback(self.items.popleft())
        else:
            self.waiting.append(lambda: self.get(callback))


def producer(q, count):
    def _run(n=0):
        if n < count:
            print(f"Producing, {n}")
            q.put(n)
            sched.call_later(1, lambda: _run(n+1))
        else:
            print("Producer done")
            q.close()  # Sentinel to shut down
    _run()


def consumer(q):
    def _consume(item):
        if item is None:
            print('Consumer done')
        else:
            print('Consuming', item)
            sched.call_soon(lambda: consumer(q))
    q.get(callback=_consume)


q = AsyncQueue()
sched.call_soon(lambda: producer(q, 10))
sched.call_soon(lambda: consumer(q))
sched.run()

"""
q = queue.Queue()  # thread-safe queue
threading.Thread(target=producer, args=(q, 10)).start()
threading.Thread(target=consumer, args=(q,)).start()
"""
