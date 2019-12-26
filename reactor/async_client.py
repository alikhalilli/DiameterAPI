import asyncio


async def printer(msg, caller, sleep):
    await asyncio.sleep(sleep)
    print(f"{caller} - {msg}\n")


async def producer():
    tasks = [printer(i, "producer", 2) for i in range(10)]
    await asyncio.gather(*tasks)


async def consumer():
    tasks = [printer(i, "consumer", 1) for i in range(10)]
    await asyncio.gather(*tasks)


class WatchDogTask:
    def __init__(self, interval):
        self._interval = interval
        self._currentTask = None

    def reset(self):
        self._currentTask.cancel()
        self._currentTask = asyncio.ensure_future(self.printer("salamsalam2"))

    def attachTask(self):
        self._currentTask = asyncio.ensure_future(self.printer("salamsalam"))

    async def printer(self, msg):
        while True:
            await asyncio.sleep(self._interval)
            print(f"-> {msg}\n")


class Peer:
    def __init__(self, wtd):
        self._watchdog = wtd
        self._watchdog.attachTask()

    def resetWatchDog(self):
        self._watchdog.reset()

    def attachWatchdog(self, wtd):
        self._watchdog = wtd


async def addPeer(peer):
    pass
    # peer.resetWatchDog()


async def main():
    peer = Peer(WatchDogTask(5))
    asyncio.ensure_future(addPeer(peer))

    #t1 = asyncio.create_task(producer())
    # await t1
    #t2 = asyncio.create_task(consumer())

    # asyncio.ensure_future(producer())
    # await asyncio.gather(t1, t2)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
