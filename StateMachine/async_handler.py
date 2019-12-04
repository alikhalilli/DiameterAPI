import asyncio


"""
base_events
coroutines
events
futures
locks
protocols
runners
queues
streams
subprocess
tasks
transports
"""


class Server:
    def __init__(self):
        pass


async def factorial(value):
    f = 1
    for i in range(value):
        f *= i
        print(f)
        return f

asyncio.run(factorial(10))
