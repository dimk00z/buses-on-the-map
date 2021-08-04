import trio
from sys import stderr
from trio_websocket import open_websocket_url


async def main():
    try:
        async with open_websocket_url('ws://127.0.0.1:8080') as ws:
            await ws.send_message('hello world!')
            message = await ws.get_message()
            print('Received message: %s' % message)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)

trio.run(main)
