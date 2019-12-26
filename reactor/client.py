import asyncio


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 9999)

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    return writer


async def client_writer(writer, message):
    writer.write(message.encode())
    await asyncio.sleep(1)


async def DWRMessage(peer=None):
    await asyncio.sleep(5)
    return "DWRMessage.."


async def CCRMessage(peer=None):
    await asyncio.sleep(1)
    return "CCRMessage.."


async def main(message):
    peerTable = []
    writer = await tcp_echo_client(message)
    await client_writer(writer, "salamsalam")
    await client_writer(writer, "neynirsen")
    while True:
        await client_writer(writer, await DWRMessage())


async def broker(msg):
    await main(msg)

asyncio.run(main("hello world"))

task = asyncio.create_task(CCRMessage())
loop = asyncio.get_running_loop()
loop.run_until_complete(task)
