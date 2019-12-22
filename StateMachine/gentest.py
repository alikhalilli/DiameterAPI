import time
import threading
from collections import deque
import heapq
import queue
import threading
import asyncio

"""
socket -> handler.send(message) -> CCN
CCN -> handler.recv() -> socket
"""

"""async def makeCCR(t=124):
    result = await message.send(peer)
    dt = t - result['grantedUnit']
    while dt % 60 > 0:
        message = makeCRR(60)
        result = await message.send(peer)
        dt = dt - result['grantedUnit']
        await asyncio.sleep(dt)
    message = makeCCR(dt)  # CCR-T
    await asyncio.sleep(dt)
    termination_result = await message.send(peer)"""


class Scheduler:
    def __init__(self):
        self.ready = deque()  # functions ready to execute
        self.sleeping = []  # sleeping functions
        self.sequence = 0

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


def countdown(n):
    if n > 0:
        print(f"Down {n}")
        sched.call_later(4, lambda: countdown(n-1))
        # time.sleep(4)
        # sched.call_soon(lambda: countdown(n-1))


def countup(stop):
    def _run(n):
        if n < stop:
            print(f"Count up {n}")
            sched.call_later(1, lambda: _run(n+1))
            # time.sleep(1)
            # sched.call_soon(lambda: _run(n+1))
    _run(0)


sched.call_soon(lambda: countdown(5))
sched.call_soon(lambda: countup(10))
sched.run()


#threading.Thread(target=countup, args=(10, )).start()
#threading.Thread(target=countdown, args=(10, )).start()


"""countdown(10)
countup(10)
"""
